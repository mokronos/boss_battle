import json
import os
from typing import Dict, List, Optional

from pydantic import BaseModel
import requests

from boss_battle.boss_generation.boss_traits import BossTraits

class Message(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class ResponseChoice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[str] = None

class ResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ResponseChoice]
    usage: ResponseUsage


class OpenRouterClient:
    def __init__(self, model: str, max_tokens: int = 1024, temperature: float = 0.7):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "boss_battle"
        }
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def get_completion(self, messages: List[Dict[str, str]]) -> CompletionResponse:
        """Get a completion from OpenRouter"""
        
        message_objects = [Message(**msg) for msg in messages]
        
        request = CompletionRequest(
            model=self.model,
            messages=message_objects,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            data=request.model_dump_json()
        )
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        response_data = response.json()
        return CompletionResponse(**response_data)

    def get_structured_output(self, prompt: str) -> BossTraits:
        """Get a structured output from OpenRouter"""
        
        system_message = {
            "role": "system",
            "content": f"""
            You are an AI that generates structured JSON output for a game boss.
            The output should be a JSON object with the following fields:
            - size: int (1-3)
            - moveSpeed: int (1-10)
            - attackSpeed: int (1-10)
            - attackDamage: int (1-100)
            - attackRange: int (1-10)
            - attackType: str (one of "melee", "ranged", "magic")
            The values should be within the specified ranges.
            The output should be a valid JSON object with no additional text.
            Example output:
            {{
                "size": 2,
                "moveSpeed": 5,
                "attackSpeed": 3,
                "attackDamage": 50,
                "attackRange": 7,
                "attackType": "magic"
            }}
            The output should be a valid JSON object with no additional text.
            Please provide the output in the same format as the example.
            Do not include any explanations or additional text.
            The output should be a valid JSON object with no additional text.
            """
        }
        
        user_message = {
            "role": "user",
            "content": prompt
        }
        
        response = self.get_completion(
            messages=[system_message, user_message],
        )
        
        try:
            content = response.choices[0].message.content
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                json_data = json.loads(json_str)
                return BossTraits(**json_data)
            else:
                raise ValueError("No valid JSON found in the response")
        except Exception as e:
            raise ValueError(f"Failed to parse structured output: {str(e)}")