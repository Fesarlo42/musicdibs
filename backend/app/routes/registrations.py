from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
import base64
import hashlib

from app.database import get_db

# pydantic models
from app.schemas import RegistrationResponse

# sqlalchemy models
from app.models import Registration as RegistrationModel, File as FileModel, Project as ProjectModel, User as UserModel

# services
from app.services.ibs_services import post_evidence, get_evidence
from app.services.files_services import upload_file, get_file, get_presigned_url
from app.services.pdf_services import generate_receipt_pdf


router = APIRouter()


# handle evidence success event
@router.post("/webhook", status_code=200, include_in_schema=False)
async def registration_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    # Parse the webhook payload
    try:
        payload = await request.json()
        
        # Extract necessary information
        data = payload.get("data", {})
        ibs_id = data.get("evidence_id")
        ibs_payload = data.get("payload", {})
        integrity = ibs_payload.get("integrity", [])[0]

        if not ibs_id or not data:
            raise HTTPException(
                status_code = 400,
                detail = "Missing required fields in webhook payload"
            )
        
        # Find the registration record
        registration = db.query(RegistrationModel).filter(
            RegistrationModel.ibs_id == ibs_id
        ).first()
        
        if not registration:
            raise HTTPException(
                status_code = 404,
                detail = f"No registration found for IBS ID {ibs_id}"
            )
        
        # Get project data
        project = db.query(ProjectModel).filter(
            ProjectModel.id == registration.project_id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code = 404,
                detail = {f"Project not found for registration {registration.id}"}
            )
        
        # Generate and upload pdf recipt
        pdf_recipt = generate_receipt_pdf(project, data)
        object_key = upload_file(pdf_recipt)

        # Add recipt record to database
        file_db = FileModel(
            project_id = project.id,
            object_key = object_key,
            name = pdf_recipt.filename,
            origin = "receipt"
        )

        # Update registration record with the checksum
        registration.file_checksum = integrity.get('checksum')
            
        db.add(file_db)
        db.commit()
        
        return {"status": "success"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = f"Error processing webhook: {str(e)}"
        )

@router.post("/verify-file", status_code=200)
async def verify_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Read the file content
        contents = await file.read()
        
        # Calculate SHA-512 checksum with base64 standard encoding
        hash_obj = hashlib.sha512(contents)
        file_checksum = base64.standard_b64encode(hash_obj.digest()).decode('utf-8')
        
        # Look for a registration with matching checksum
        registration = db.query(RegistrationModel).filter(
            RegistrationModel.file_checksum == file_checksum
        ).first()
        
        if not registration:
            return {
                "status": "failure",
                "message": "No matching registration found"
            }
        
        # Get associated project
        project = db.query(ProjectModel).filter(
            ProjectModel.id == registration.project_id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=404,
                detail=f"Project not found for registration {registration.id}"
            )
        
        # Get user info
        user = db.query(UserModel).filter(
            UserModel.id == project.user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User not found for registration {registration.id}"
            )
        
        # Get registration prof download url
        registration_file = db.query(FileModel).filter(
            FileModel.project_id == project.id,
            FileModel.origin == "receipt"
        )

        if registration_file is None:
            raise HTTPException(
                status_code=404,
                detail=f"Registration file not found for project {project.id}"
            )
        
        # Generate presigned URL for the registration file
        presigned_url = get_presigned_url(registration_file.object_key)


        # Return basic project information
        return {
            "status": "success",
            "registration_id": registration.id,
            "registered_at": registration.registered_at,
            "registration_proof": presigned_url,
            "project": {
                "id": project.id,
                "name": project.name,
                "author": f"{user.first_name} {user.last_name}",
            }
        }
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying file: {str(e)}"
        )
    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)

@router.post("/{project_id}", response_model=RegistrationResponse, status_code=201)
async def create_registration(
    project_id: int,
    db: Session = Depends(get_db)
):  
    # Verify if project exists
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    title = project.name
    
    # Find appropriate files for the project (user_upload or ai_generated)
    files = db.query(FileModel).filter(
        FileModel.project_id == project_id,
        FileModel.origin.in_(['user_upload', 'ai_generated'])
    ).all()
    
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No valid files found for registration"
        )
    
    # Prepare files array and close them after reading
    files_with_base64 = []

    try:
        for file_db in files:
            # Get file from storage
            file_content = get_file(file_db.object_key)
            
            # Base64 encode the file content
            base64_content = base64.b64encode(file_content).decode("utf-8")
            
            # Append file data and name to the list
            files_with_base64.append({
                "name": file_db.name,
                "file": base64_content
            })
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve or process files from storage: {str(e)}"
        )
    
    # Get user ibs_sig for registration
    user = db.get(UserModel, project.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare data for IBS API
    data = {
        "payload": {
            "title": title,
            "files": files_with_base64
        },
        "signatures": [
            {"id": user.ibs_sig}
        ]
    }
    
    # Call IBS API to create evidence
    try:
        evidence_response = await post_evidence(data)

        print(evidence_response)

        ibs_id = evidence_response.get('id')
        
        if not ibs_id:
            raise HTTPException(
                status_code=500,
                detail="Failed to get IBS ID from response"
            )
        
        registration = RegistrationModel(
            project_id=project_id,
            ibs_id=ibs_id
        )
        
        db.add(registration)
        db.commit()
        db.refresh(registration)
        
        return registration
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_registration(
    project_id: int,
    db: Session = Depends(get_db)
):    
    # Verify project exists
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code = 404,
            detail = f"Project with ID {project_id} not found"
        )
    
    # Find registration for the project
    registration = db.query(RegistrationModel).filter(
        RegistrationModel.project_id == project_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code = 404,
            detail = f"No registration found for project with ID {project_id}"
        )
    
    # Find receipt file for this project if it exists
    receipt_file = db.query(FileModel).filter(
        FileModel.project_id == project_id,
        FileModel.origin == "receipt"
    ).first()

    receipt_url = None
    if receipt_file:
        # Generate presigned URL for the receipt
        try:
            receipt_url = get_presigned_url(receipt_file.object_key)
        except Exception as e:
            # Log the error but continue with the rest of the response
            print(f"Error generating presigned URL: {str(e)}")

    # Call IBS API to get evidence details
    try:
        evidence_details = await get_evidence(registration.ibs_id)
        
        # Combine database info with API response
        result = {
            "id": registration.id,
            "ibs_id": registration.ibs_id,
            "project_id": registration.project_id,
            "registered_at": registration.registered_at,
            "evidence_details": evidence_details,
            "receipt_url": receipt_url
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code = 502,
            detail = f"Failed to get evidence details: {str(e)}"
        )
