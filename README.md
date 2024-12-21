# PollinationsAI Python Client

## Overview
A robust, type-safe Python client for interacting with PollinationsAI services. This client provides a clean, object-oriented interface for both chat and image generation capabilities, with comprehensive error handling and input validation.

⚠️ **Educational Purpose Disclaimer:**
This code is provided strictly for educational and learning purposes. It is designed to demonstrate modern Python programming practices, API client implementation, and software design patterns. Any use of this code to harm, disrupt, or disrespect PollinationsAI's services or infrastructure is strictly prohibited. Users are responsible for ensuring their usage complies with PollinationsAI's terms of service and API policies.

## Features
- 🤖 Chat API integration with system prompt support
- 🎨 Image generation with multiple model options
- ✨ Type-safe implementation with proper validation
- 🛡️ Comprehensive error handling
- 📝 Full API documentation
- 🧩 Modular and extensible design

## Requirements
```
python >= 3.7
cloudscraper
typing
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/sujalrajpoot/PollinationsAI-Python-Client.git
cd PollinationsAI-Python-Client
```

2. Install dependencies:
```bash
pip install cloudscraper
```

## Quick Start

### Basic Usage
```python
from pollinations_ai import PollinationsAI, ModelType

# Initialize client
client = PollinationsAI()

# Chat example
try:
    response = client.chat("What is artificial intelligence?")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")

# Generate image
try:
    result = client.generate_image(
        prompt="A serene lake at sunset with mountains in the background",
        model=ModelType.FLUX_3D,
        image_path="sunset_lake.png"
    )
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

### Available Models
The client supports multiple AI models for image generation:
- Flux
- Flux Realism
- Any Dark
- Flux Anime
- Flux 3D
- Turbo

## Detailed Documentation

### PollinationsAI Class
The main client class that provides access to both chat and image generation services.

```python
class PollinationsAI:
    def __init__(self, timeout: int = 10):
        """Initialize with custom timeout if needed"""
        
    def chat(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """Send a chat request"""
        
    def generate_image(
        self,
        prompt: str,
        model: ModelType = ModelType.FLUX_3D,
        image_path: str = "image.png",
        width: int = 1024,
        height: int = 1024,
        enhance: bool = True
    ) -> str:
        """Generate an image with specified parameters"""
```

### Error Handling
The client includes a comprehensive error handling system:
```python
try:
    response = client.chat("Hello")
except PollinationsError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### Image Generation
1. Use descriptive prompts for better results
2. Consider image dimensions for your use case
3. Enable enhancement for better quality
4. Use appropriate model for your desired style

### Chat Integration
1. Provide clear, concise prompts
2. Use system prompts to guide AI behavior
3. Handle responses appropriately
4. Implement proper error handling

## Acknowledgments
- Thanks to PollinationsAI for their innovative AI services
- Contributors to the cloudscraper library
- The Python community for type hinting support

## FAQ
**Q: Is this an official client?**  
A: No, this is an unofficial client for educational purposes only.

**Q: Can I use this in production?**  
A: This client is for educational purposes only and should not be used in production environments.

**Q: How can I contribute?**  
A: See the Contributing section above.

---

**Remember**: This code is for educational purposes only. Use responsibly and ethically. Use responsibly and respect API limitations! 🚀

---

Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
