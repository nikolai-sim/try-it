import os
import base64
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv('STABILITY_API_KEY')
API_HOST = os.getenv("API_HOST", "https://api.stability.ai")
ENGINE_ID = "stable-diffusion-v1-6"

if API_KEY is None:
    raise Exception("Missing Stability API key.")

def main():
    parser = argparse.ArgumentParser(description="Merge two images using Stability AI API")
    parser.add_argument('image1', type=str, help="Path to the first image")
    parser.add_argument('image2', type=str, help="Path to the second image")
    args = parser.parse_args()

    # Define the API endpoint and headers
    url = f"{API_HOST}/v1/generation/{ENGINE_ID}/image-to-image"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Create the payload
    files = {
        'init_image': open(args.image1, 'rb')
    }
    data = {
        "image_strength": 0.75,
        "init_image_mode": "IMAGE_STRENGTH",
        "text_prompts[0][text]": "Combine the two images so that the image of the person is wearing the sunglasses in the second image",
        "cfg_scale": 7,
        "samples": 1,
        "steps": 50,
    }

    # Make the request
    response = requests.post(url, headers=headers, files=files, data=data)

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        for i, artifact in enumerate(result['artifacts']):
            image_data = base64.b64decode(artifact['base64'])
            with open(f'output_image_{i}.png', 'wb') as output_file:
                output_file.write(image_data)
        print("Image generated successfully and saved as output_image_0.png")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()