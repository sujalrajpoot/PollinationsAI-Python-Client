from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import cloudscraper
import random
from http import HTTPStatus
import json

class PollinationsError(Exception):
    """Base exception class for Pollinations AI related errors."""
    pass

class APIError(PollinationsError):
    """Exception raised for API related errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class ValidationError(PollinationsError):
    """Exception raised for input validation errors."""
    pass

class ModelType(Enum):
    """Enumeration of available AI models."""
    FLUX = "flux"
    FLUX_REALISM = "flux-realism"
    ANY_DARK = "any-dark"
    FLUX_ANIME = "flux-anime"
    FLUX_3D = "flux-3d"
    TURBO = "turbo"

    @classmethod
    def get_display_name(cls, model: 'ModelType') -> str:
        """Convert enum value to display name."""
        return {
            cls.FLUX: "Flux",
            cls.FLUX_REALISM: "Flux Realism",
            cls.ANY_DARK: "Any Dark",
            cls.FLUX_ANIME: "Flux Anime",
            cls.FLUX_3D: "Flux 3D",
            cls.TURBO: "Turbo"
        }[model]

@dataclass
class RequestHeaders:
    """Data class for common request headers."""
    accept: str
    accept_language: str = "en-US,en;q=0.5"
    content_type: Optional[str] = None
    origin: Optional[str] = None
    priority: Optional[str] = None
    referer: str = "https://karma.pollinations.ai/"
    sec_ch_ua: str = '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
    sec_ch_ua_mobile: str = "?0"
    sec_ch_ua_platform: str = '"Windows"'
    sec_fetch_site: str = "same-site"
    sec_gpc: str = "1"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    def to_dict(self) -> Dict[str, str]:
        """Convert headers to dictionary format."""
        # Filter out None values and convert to dict
        return {k.replace('_', '-'): v for k, v in self.__dict__.items() if v is not None}

class BaseClient(ABC):
    """Abstract base class for API clients."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the base client.
        
        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        self.scraper = cloudscraper.create_scraper()
        self.timeout = timeout

    @abstractmethod
    def validate_response(self, response: Any) -> None:
        """
        Validate API response.
        
        Args:
            response: Response from the API
        
        Raises:
            APIError: If the response is invalid
        """
        pass

class ChatClient(BaseClient):
    """Client for interacting with Pollinations AI chat API."""

    def __init__(self, timeout: int = 10):
        """
        Initialize the chat client.
        
        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        super().__init__(timeout)
        self.base_url = "https://text.pollinations.ai/"

    def validate_response(self, response: Any) -> None:
        """Validate chat API response."""
        if response.status_code != HTTPStatus.OK:
            raise APIError(response.status_code, response.text)

    def chat(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Send a chat request to the API.
        
        Args:
            prompt (str): User's input prompt
            system_prompt (str): System prompt to guide the AI's behavior
            
        Returns:
            str: AI's response
            
        Raises:
            APIError: If the API request fails
            ValidationError: If input validation fails
        """
        assert isinstance(prompt, str) and prompt.strip(), "Prompt must be a non-empty string"
        assert isinstance(system_prompt, str), "System prompt must be a string"

        headers = RequestHeaders(
            accept="*/*",
            content_type="application/json",
            origin="https://karma.pollinations.ai",
            priority="u=1, i"
        ).to_dict()

        json_data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "jsonMode": True,
            "seed": str(random.randint(10, 99))
        }

        response = self.scraper.post(
            self.base_url,
            headers=headers,
            json=json_data,
            timeout=self.timeout
        )
        
        self.validate_response(response)
        return response.content.decode('utf-8')

class ImageClient(BaseClient):
    """Client for interacting with Pollinations AI image generation API."""

    def __init__(self, timeout: int = 10):
        """
        Initialize the image generation client.
        
        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        super().__init__(timeout)
        self.base_url = "https://pollinations.ai/p/"

    def validate_response(self, response: Any) -> None:
        """Validate image API response."""
        if response.status_code != HTTPStatus.OK:
            raise APIError(response.status_code, response.text)
        if not response.content:
            raise APIError(response.status_code, "Empty response received")

    def generate_image(
        self,
        prompt: str,
        model: ModelType = ModelType.FLUX_3D,
        image_path: str = "image.png",
        width: int = 1024,
        height: int = 1024,
        enhance: bool = True
    ) -> str:
        """
        Generate an image using the API.
        
        Args:
            prompt (str): Description of the image to generate
            model (ModelType): AI model to use for generation
            image_path (str): Path to save the generated image
            width (int): Image width in pixels
            height (int): Image height in pixels
            enhance (bool): Whether to enhance the image
            
        Returns:
            str: Success message with save location
            
        Raises:
            APIError: If the API request fails
            ValidationError: If input validation fails
        """
        assert isinstance(prompt, str) and prompt.strip(), "Prompt must be a non-empty string"
        assert isinstance(model, ModelType), "Model must be a ModelType enum"
        assert isinstance(width, int) and width > 0, "Width must be a positive integer"
        assert isinstance(height, int) and height > 0, "Height must be a positive integer"
        assert isinstance(enhance, bool), "Enhance must be a boolean"

        headers = RequestHeaders(
            accept="image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            priority="i"
        ).to_dict()

        params = {
            "width": width,
            "height": height,
            "model": model.value,
            "seed": str(random.randint(10, 99)),
            "nologo": "true",
            "enhance": str(enhance).lower(),
        }

        response = self.scraper.get(
            f"{self.base_url}{prompt.replace(' ', '%20')}",
            headers=headers,
            params=params,
            timeout=self.timeout
        )
        
        self.validate_response(response)
        
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        return f"Image successfully saved to {image_path}"

class PollinationsAI:
    """Main class for interacting with Pollinations AI services."""

    def __init__(self, timeout: int = 10):
        """
        Initialize Pollinations AI client.
        
        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        self.chat_client = ChatClient(timeout)
        self.image_client = ImageClient(timeout)

    def chat(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """Wrapper for ChatClient.chat()"""
        return self.chat_client.chat(prompt, system_prompt)

    def generate_image(
        self,
        prompt: str,
        model: ModelType = ModelType.FLUX_3D,
        image_path: str = "image.png",
        width: int = 1024,
        height: int = 1024,
        enhance: bool = True
    ) -> str:
        """Wrapper for ImageClient.generate_image()"""
        return self.image_client.generate_image(prompt, model, image_path, width, height, enhance)

# Example usage
if __name__ == "__main__":
    client = PollinationsAI()
    
    # Chat example
    try:
        response = client.chat("Hi")
        print(f"Chat Response: {response}")
    except PollinationsError as e:
        print(f"Chat Error: {e}")

    # Image generation example
    try:
        result = client.generate_image(
            "A Red colour dodge challenger on street road at night with some neon lights",
            model=ModelType.FLUX_3D
        )
        print(f"Image Result: {result}")
    except PollinationsError as e:
        print(f"Image Generation Error: {e}")