import json
import httpx
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

async def fetch_text_from_mcp(file_path: str):
    """Fetches text content from the MCP server."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MCP_SERVER_URL}/read-text-from-file",
            params={"file_path": file_path},  # Using GET request with params
        )
        if response.status_code == 200:
            data = response.json()
            return data if data else "Failed to fetch data"
        else:
            return f"Error: {response.status_code}, {response.text}"

def generate_gemini_response(text: str):
    """Calls Gemini API to process and format the text."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Format and summarize this:\n{text}")
    return response.text

async def main():
    file_path = "data.txt"  # Change to the correct file path
    text_content = await fetch_text_from_mcp(file_path)
    print("text_content--------",text_content)
    if text_content:
        formatted_response = generate_gemini_response(text_content)
        print("=== Processed Response ===")
        print(formatted_response)
    else:
        print("Failed to read file.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
