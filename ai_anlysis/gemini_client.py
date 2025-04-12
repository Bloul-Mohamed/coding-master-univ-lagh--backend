import json
import os
from typing import Dict, Any, Optional, Tuple, Union

import google.generativeai as genai
from django.conf import settings


class GeminiClient:
    """Client for interacting with Google's Gemini API"""

    def __init__(self):
        # Get API key from settings or environment variable
        api_key = getattr(settings, 'GEMINI_API_KEY',
                          os.environ.get('GEMINI_API_KEY'))
        if not api_key:
            raise ValueError(
                "Gemini API key is not set. Please set GEMINI_API_KEY in settings or environment variables.")

        # Configure the Gemini API
        genai.configure(api_key=api_key)

        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini API"""
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

    async def improve_description(self, project_data: Dict[str, Any]) -> str:
        """Improve project description"""
        from .prompts import GeminiPrompts
        prompt = GeminiPrompts.improve_description_prompt(project_data)
        return await self.generate_content(prompt)

    async def score_idea(self, project_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Score project idea and return overall score with details"""
        from .prompts import GeminiPrompts
        prompt = GeminiPrompts.score_idea_prompt(project_data)
        response = await self.generate_content(prompt)

        try:
            score_data = json.loads(response)
            overall_score = score_data.get('overall_score', 0.0)
            return overall_score, score_data
        except json.JSONDecodeError:
            # If response is not valid JSON, return default values
            print(f"Invalid JSON response: {response}")
            return 0.0, {}

    async def get_suggestions(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get suggestions for the project"""
        from .prompts import GeminiPrompts
        prompt = GeminiPrompts.suggestions_prompt(project_data)
        response = await self.generate_content(prompt)

        try:
            suggestions_data = json.loads(response)
            return suggestions_data
        except json.JSONDecodeError:
            # If response is not valid JSON, return empty dict
            print(f"Invalid JSON response: {response}")
            return {}
