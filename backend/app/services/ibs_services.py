import httpx
import json

import os

ibs_url = os.getenv("IBS_BASE_URL")

def get_auth_headers() -> dict:
    ibs_token = os.getenv("IBS_ACCESS_TOKEN")
    return {"Authorization": f"Bearer {ibs_token}"}


# digital identity
async def post_signature(params: dict) -> dict:
    # TODO: add urls after deployment
    params["wizard"] = {
        "ok_url": '',
        "ko_url": ''
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ibs_url}/signatures", 
            json=params,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

async def put_signature(sig_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{ibs_url}/signatures/{sig_id}",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
async def get_signature(sig_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ibs_url}/signatures/{sig_id}",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

async def delete_signature(sig_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{ibs_url}/signatures/{sig_id}",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()


# blockchain registration
async def post_evidence(data: dict) -> dict:        
    async with httpx.AsyncClient() as client:
        print(json.dumps(data))
        response = await client.post(
            f"{ibs_url}/evidences",
            json=data,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()


async def get_evidence(evd_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ibs_url}/evidences/{evd_id}",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()