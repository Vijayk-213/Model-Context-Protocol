import os
import json
import httpx
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

async def fetch_text_from_mcp(file_path: str):
    """Send file path to MCP server to read the file"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MCP_SERVER_URL}/mcp",
            json={
                "input": "read_file",  # Send correct tool name
                "context": {
                    "file": file_path  # Ensure the key matches what the server expects
                }
            }
        )
        if response.status_code == 200:
            return response.json().get("output")
        else:
            return f"Error: {response.status_code} - {response.text}"

def generate_gemini_response(text: str, query: str):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Use the context:\n{text}\n\nQuestion: {query}")
    return response.text

async def main():
    file_path = "data.txt"
    text_content = await fetch_text_from_mcp(file_path)
    print("text_content--------", text_content)

    if text_content:
        query = "Provide the sum of salaries of Alice Johnson and Bob Smith"
        result = generate_gemini_response(text_content, query)
        print("\n=== Gemini Response ===\n", result)
    else:
        print("Failed to read file content.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
