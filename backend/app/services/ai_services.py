import google.generativeai as genai
import os

from typing import List, Dict, Any

gemini_key = os.getenv("GOOGLE_API_KEY")
gemini_model = "gemini-1.5-pro"

class GeminiService:
    @staticmethod
    def get_model():
        return genai.GenerativeModel(gemini_model)
    
    @staticmethod
    async def generate_initial_content(conversation_data, user_message):
        model = GeminiService.get_model()

        # Combine system prompt with user message
        full_prompt = f"""Eres un creador musical experto que colabora en la composición musical.
    Propósito: {conversation_data.purpose}
    Tempo: {conversation_data.tempo} BPM
    Armadura de tonalidad: {conversation_data.key_signature}
    Estado de ánimo: {conversation_data.mood}

    Ofrece contenido musical creativo y apropiado que se ajuste a estos parámetros.
    Céntrate en ser muy específico y apropiado para el contexto musical proporcionado.
    Incluye siempre tu contenido musical final claramente marcado con:

    --- CONTENIDO FINAL---
    [Tu contenido musical aquí]
    --- CONTENIDO FINAL---

    Esto ayuda al usuario a distinguir entre tus explicaciones y el contenido musical real.

    Usuario: {user_message}
    """

        try:
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")


    @staticmethod
    async def continue_conversation(conversation_data, message_history, new_message):
        model = GeminiService.get_model()
        
        conversation_text = f"""Eres un creador musical experto que colabora en la composición musical.
        Propósito: {conversation_data.purpose}
        Tempo: {conversation_data.tempo} BPM
        Armadura de tonalidad: {conversation_data.key_signature}
        Estado de ánimo: {conversation_data.mood}

        Continúa la conversación mientras te concentras en estos parámetros musicales.
        Marca siempre el contenido musical con:

        --- CONTENIDO FINAL---
        [Tu contenido musical aquí]
        --- CONTENIDO FINAL---

        Esto ayuda al usuario a distinguir entre sus explicaciones y el contenido musical real.
        """
        
        for msg in message_history:
            speaker = "Usuario" if not msg.is_from_ai else "IA"
            conversation_text += f"\n{speaker}: {msg.content}"

        conversation_text += f"\nUsuario: {new_message}"
        
        try:
            response = model.generate_content(conversation_text)
            return response.text
        except Exception as e:
            raise Exception(f"Error continuing conversation: {str(e)}")


    @staticmethod
    async def export_to_file(conversation_data, messages):
        ai_messages = [msg for msg in messages if msg.is_from_ai]
        
        if not ai_messages:
            raise Exception("No AI-generated content found to export")
        
        last_ai_message = ai_messages[-1]
        content = last_ai_message.content
        
        # Extract the content between the markers
        import re
        content_match = re.search(r'--- CONTENIDO FINAL---\s*([\s\S]*?)\s*--- CONTENIDO FINAL---', content)
        
        if content_match:
            final_content = content_match.group(1).strip()
        else:
            # If markers not found, use the whole content
            final_content = content
        
        header = f"""Titulo: {conversation_data.purpose}
        Tempo: {conversation_data.tempo}
        Armadura de tonalidade: {conversation_data.key_signature}
        Estado do ánimo: {conversation_data.mood}

        """
        
        return header + final_content