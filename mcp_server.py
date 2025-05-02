from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
import uvicorn
import os

# Initialize FastAPI application
app = FastAPI()

# Ensure data.txt exists
FILE_PATH = "data.txt"
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write("Alice Johnson, 5000\nBob Smith, 4500\n")

# Create MCP instance
mcp = FastMCP("filesystem")

# Define the tool for reading the file
@mcp.tool()
async def read_file_tool(input_data: dict) -> str:
    """Reads text content from a given file path"""
    print(f"Received input_data: {input_data}")  # Log the input data
    try:
        file_path = input_data.get("file")
        if not file_path:
            return "No file path provided in the context."

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        _, file_ext = os.path.splitext(file_path)
        if file_ext not in [".txt", ".log"]:
            return f"Unsupported file format: {file_ext}"

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return f"Error reading file: {str(e)}"

# MCP endpoint
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    data = await request.json()
    print(f"Received request data: {data}")  # Log the incoming request
    input_text = data.get("input", "")
    context = data.get("context", {})

    try:
        # Directly call the read_file_tool instead of mcp.run()
        if input_text == "read_file" and "file" in context:
            result = await read_file_tool(context)
            return {"output": result}
        else:
            return {"error": "Invalid input or context"}
    except Exception as e:
        return {"error": str(e)}

# Health check route
@app.get("/")
def root():
    return {"message": "MCP Server is running."}

# Run the server
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
