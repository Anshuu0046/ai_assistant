import os
import google.generativeai as genai
from datetime import datetime
from models import ChatResponse

# Configure Gemini API
# In a real production app, use os.getenv("GEMINI_API_KEY")
# For this demo, we are setting it directly as requested, but normally we'd use a .env file.
GEMINI_API_KEY = "AIzaSyDvNRv_UAj1UQweoT5OI-h5c1tymDSHUmA"
genai.configure(api_key=GEMINI_API_KEY)

class ChatService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat_session = self.model.start_chat(history=[])

    def get_response(self, user_message: str, model_name: str = "gemini-2.0-flash", persona: str = "default", image_data: str = None) -> str:
        """
        Generates a response using Google's Gemini API with optional image and persona.
        """
        try:
            # Configure System Instruction (Persona)
            system_instruction = ""
            if persona == "pirate":
                system_instruction = "You are a helpful AI assistant, but you talk like a pirate. Use terms like 'Ahoy', 'Matey', and 'Shiver me timbers'."
            elif persona == "disney":
                system_instruction = "You are a magical, cheerful Disney-style guide. You are optimistic, use emojis ✨, and reference magic and dreams."
            elif persona == "professional":
                system_instruction = "You are a strictly professional corporate assistant. Be concise, formal, and objective."
            
            # Initialize model
            # Note: system_instruction is supported in newer models/SDKs. 
            # If not supported by the specific model version, we can prepend it to the prompt.
            model = genai.GenerativeModel(model_name)

            content_parts = []
            
            # Add system instruction to prompt (simplest way to ensure compatibility)
            if system_instruction:
                content_parts.append(system_instruction + "\n\nUser: " + user_message)
            else:
                content_parts.append(user_message)

            # Add Image if present
            if image_data:
                import base64
                from io import BytesIO
                from PIL import Image
                
                # Remove header if present (e.g., "data:image/jpeg;base64,")
                if "," in image_data:
                    image_data = image_data.split(",")[1]
                
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                content_parts.append(image)

            response = model.generate_content(content_parts)
            return response.text
        except Exception as e:
            return f"Error ({model_name}): {str(e)}"

chat_service = ChatService()
