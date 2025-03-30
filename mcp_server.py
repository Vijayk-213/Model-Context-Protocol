from typing import Any, Union, List
import httpx
from mcp.server.fastmcp import FastMCP
import os
import shutil
import aiofiles
import asyncio
from pathlib import Path
import csv
from docx import Document
import pandas as pd
import json
import xml.etree.ElementTree as ET
from fastapi import FastAPI
import uvicorn

app = FastAPI()
mcp = FastMCP("filesystem")

# @app.get("/create-file")
# async def create_file(file_path: str, content: str = "") -> bool:
#     try:
#         async with aiofiles.open(file_path, mode='w') as f:
#             await f.write(content)
#         return True
#     except Exception as e:
#         print(f"File creation failed: {e}")
#         return False

# @app.get("/save-file")
# async def save_file(file_path: str, content: str, file_format: str = "txt") -> bool:
#     try:
#         if not file_path.endswith(f".{file_format}"):
#             file_path = f"{file_path}.{file_format}"
#         async with aiofiles.open(file_path, mode='w') as f:
#             await f.write(content)
#         return True
#     except Exception as e:
#         print(f"File save failed: {e}")
#         return False

# @app.get("/copy-file")
# async def copy_file(src: str, dst: str) -> bool:
#     try:
#         shutil.copy2(src, dst)
#         return True
#     except Exception as e:
#         print(f"File copy failed: {e}")
#         return False

# @app.get("/move-file")
# async def move_file(src: str, dst: str) -> bool:
#     try:
#         shutil.move(src, dst)
#         return True
#     except Exception as e:
#         print(f"File move failed: {e}")
#         return False

# @app.get("/batch-copy-files")
# async def batch_copy_files(src_paths: List[str], dst_dir: str) -> List[bool]:
#     results = []
#     for src in src_paths:
#         dst = os.path.join(dst_dir, os.path.basename(src))
#         success = await copy_file(src, dst)
#         results.append(success)
#     return results

# @app.get("/delete-file")
# async def delete_file(file_path: str, permanent: bool = False) -> bool:
#     try:
#         if permanent:
#             os.unlink(file_path)
#         else:
#             os.remove(file_path)
#         return True
#     except Exception as e:
#         print(f"File deletion failed: {e}")
#         return False

# @app.get("/create-folder")
# async def create_folder(folder_path: str) -> bool:
#     try:
#         os.makedirs(folder_path, exist_ok=True)
#         return True
#     except Exception as e:
#         print(f"Folder creation failed: {e}")
#         return False

@app.get("/read-text-from-file")
def read_text_from_file(file_path: str) -> Union[str, None]:
    try:
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return None

        _, file_ext = os.path.splitext(file_path)

        if file_ext in (".txt", ".log", ".md", ".ini", ".cfg"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        elif file_ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.dumps(json.load(f), indent=4, ensure_ascii=False)

        elif file_ext == ".xml":
            tree = ET.parse(file_path)
            return ET.tostring(tree.getroot(), encoding="unicode")

        elif file_ext in (".csv", ".tsv"):
            delimiter = "," if file_ext == ".csv" else "\t"
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=delimiter)
                return "\n".join([delimiter.join(row) for row in reader])

        elif file_ext in (".docx", ".doc"):
            return "\n".join([p.text for p in Document(file_path).paragraphs])

        else:
            print(f"Unsupported file format: {file_ext}")
            return None
    except Exception as e:
        print(f"File read failed: {e}")
        return None

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
