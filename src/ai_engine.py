import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

try:
    from . import prompts
except ImportError:
    import prompts

class LearnBuddyEngine:
    def __init__(self):
        # The unified SDK automatically finds GEMINI_API_KEY in environment variables
        self.client = genai.Client()
        self.model_id = 'gemini-2.5-flash'
        
        # Establishing our agent framework via System Instructions
        self.system_instruction = prompts.SYSTEM_INSTRUCTION
        self.chat = None

    def start_learning_session(self, user_concept: str, user_profile: str) -> str:
        """Initializes a guided learning track and returns the first response."""
        # Try initializing with thinking_config first, fallback to standard config if not supported
        try:
            config = types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=1024)
            )
            self.chat = self.client.chats.create(
                model=self.model_id,
                config=config
            )
            prompt = prompts.get_initial_prompt(user_concept, user_profile)
            response = self.chat.send_message(prompt)
            return response.text
        except Exception:
            # Fallback if thinking_config is not supported by the model
            config = types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
            )
            self.chat = self.client.chats.create(
                model=self.model_id,
                config=config
            )
            prompt = prompts.get_initial_prompt(user_concept, user_profile)
            response = self.chat.send_message(prompt)
            return response.text

    def send_message(self, message: str) -> str:
        """Sends a message to the active chat session and returns the model's response."""
        if not self.chat:
            raise ValueError("No active learning session. Call start_learning_session first.")
        response = self.chat.send_message(message)
        return response.text