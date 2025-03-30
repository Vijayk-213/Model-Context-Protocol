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
