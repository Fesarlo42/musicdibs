import google.generativeai as genai
import os
import re
from typing import List, Dict, Any

gemini_key = os.getenv("GOOGLE_API_KEY")
gemini_model = "gemini-1.5-pro"

class GeminiService:
    @staticmethod
    def get_model():
        genai.configure(api_key=gemini_key)
        return genai.GenerativeModel(gemini_model)
    
    @staticmethod
    def extract_final_content(content):
        content_match = re.search(r'--- LA OBRA ---\s*([\s\S]*?)\s*--- LA OBRA ---', content)
        if content_match:
            return content_match.group(1).strip()
        return None
    
    @staticmethod
    def collect_all_content(message_history):
        all_content = []
        for msg in message_history:
            if msg.is_from_ai:
                content = GeminiService.extract_final_content(msg.content)
                if content:
                    all_content.append(content)
        return "\n\n".join(all_content) if all_content else ""
    
    @staticmethod
    async def generate_initial_content(conversation_data, user_message):
        model = GeminiService.get_model()

        # Combine system prompt with user message
        full_prompt = f"""Eres un creador musical experto que colabora en la composición musical.
    Propósito: {conversation_data.purpose}
    Tempo: {conversation_data.tempo} BPM
    Armadura de tonalidad: {conversation_data.key_signature}
    Estado de ánimo: {conversation_data.mood}
    Género: {conversation_data.genres}

    Ofrece contenido musical creativo y apropiado que se ajuste a estos parámetros.
    Céntrate en ser muy específico y apropiado para el contexto musical proporcionado.
    
    Incluye siempre tu contenido musical final claramente marcado con:

    --- LA OBRA ---
    [Tu contenido musical aquí]
    --- LA OBRA ---

    Este contenido debe ser acumulativo. Cada vez que generes nuevo contenido, debes incorporarlo 
    a todo lo anterior. No empieces desde cero cada vez.

    Esto ayuda al usuario a distinguir entre tus explicaciones y el contenido musical real.

    Cuando termines tu respuesta siempre avise al usuario que si esta contento con el contenido generado, pinche el botón de finalizar la conversación para generar un archivo para registrar.

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
        
        # Get previous generated content
        all_previous_content = GeminiService.collect_all_content(message_history)
        
        # Check if the user is asking for completion or final version
        completion_signals = [
            "está perfecto", "esta perfecto", "finalizar", "terminar", 
            "completo", "listo", "terminado", "acabado", "finalizado"
        ]
        
        is_completion_request = any(signal in new_message.lower() for signal in completion_signals)
        
        if is_completion_request:
            # If user signals completion, return the final complete version
            conversation_text = f"""Eres un creador musical experto.
            
            El usuario indica que está satisfecho con el trabajo realizado hasta ahora.
            
            Por favor, proporciona la versión COMPLETA Y FINAL de todo el contenido musical 
            que has creado durante esta conversación. Incluye todas las partes anteriores
            combinadas de manera coherente y organizada.
            
            Aquí está todo el contenido acumulado hasta ahora:

            {all_previous_content}
            
            Responde ÚNICAMENTE con la versión final completa entre los marcadores:
            
            --- LA OBRA ---
            [Versión completa y final de todo el contenido musical]
            --- LA OBRA ---
            
            Usuario: {new_message}
            """
        else:
            # Continue normal conversation
            conversation_text = f"""Eres un creador musical experto que colabora en la composición musical.
            Propósito: {conversation_data.purpose}
            Tempo: {conversation_data.tempo} BPM
            Armadura de tonalidad: {conversation_data.key_signature}
            Estado de ánimo: {conversation_data.mood}

            IMPORTANTE: Todo el contenido que crees debe ser ACUMULATIVO. Debes construir sobre
            el trabajo anterior, no empezar de nuevo. Cada nueva respuesta debe incluir
            y mejorar el contenido previo.
            
            Aquí está todo el contenido musical que has generado hasta ahora:
            
            {all_previous_content}
            
            Continúa la conversación mientras te concentras en estos parámetros musicales.
            Marca siempre el contenido musical COMPLETO Y ACUMULADO con:

            --- LA OBRA ---
            [Todo tu contenido musical aquí, incluyendo lo anterior y lo nuevo]
            --- LA OBRA ---

            Esto ayuda al usuario a distinguir entre tus explicaciones y el contenido musical completo.
            Cuando termines tu respuesta siempre avise al usuario que si esta contento con el contenido generado, pinche el botón de finalizar la conversación para generar un archivo para registrar.
            """
            
            # Add the last 4 messages for context
            for msg in message_history[-4:]:
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
        
        # First try to find content in the last AI message
        last_ai_message = ai_messages[-1]
        content = last_ai_message.content
        
        final_content = GeminiService.extract_final_content(content)
        
        # If no marked content in the last message, try the second to last
        if not final_content:
            last_ai_message = ai_messages[-1]
            content = last_ai_message.content
            
            final_content = GeminiService.extract_final_content(content)
        
        # If still no content, use all marked content
        if not final_content:
            final_content = GeminiService.collect_all_content(ai_messages)

        header = f"""Titulo: {conversation_data.purpose}
Tempo: {conversation_data.tempo}
Armadura de tonalidad: {conversation_data.key_signature}
Estado de ánimo: {conversation_data.mood}

"""
        
        return header + final_content