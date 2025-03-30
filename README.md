# 🚀 MCP File System API

## 📌 Overview
This project implements an **MCP (Model Context Protocol) Server** that allows interaction with a **file system** via HTTP requests. It supports **file creation, reading, copying, moving, and deletion** using FastAPI. Additionally, it integrates with **Google Gemini API** to process and summarize file contents.

---

## 📂 Features 
✅ Read various file formats (**.txt, .csv, .json, .xml, .docx**)  
✅ Stream large files efficiently  
✅ Integrate with **Google Gemini API** for text summarization  
✅ Cloud Run deployment support

---

## 🛠️ Tech Stack
- **Python 3.9+**
- **FastAPI**
- **MCP (Model Context Protocol)**
- **Google Gemini API**
- **Uvicorn** (ASGI Server)
- **httpx** (Async HTTP requests)
- **aiofiles** (Async File Handling)
- **Docker & Cloud Run**

---

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**
```bash
$ git clone https://github.com/Vijayk-213/Model-Context-Protocol.git
$ cd Model-Context-Protocol
```

### 2️⃣ **Set Up a Virtual Environment**
```bash
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ **Install Dependencies**
```bash
$ pip install -r requirements.txt
```

### 4️⃣ **Set Environment Variables**
Create a `.env` file and add your **Google Gemini API Key**:
```env
MCP_SERVER_URL=http://127.0.0.1:8000
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🔄 Running the Application

### **Start the MCP Server**
```bash
$ uvicorn mcp_server:app --host 127.0.0.1 --port 8000 --reload
```

### **Run the Main Application**
```bash
$ python main.py
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------------|---------------------------------|
| `GET` | `/read-text-from-file?file_path=path.txt` | Read file contents |
| `POST` | `/invoke` | Call MCP function |

---

## 🛠️ Future Enhancements
✅ Implement WebSockets for real-time file updates  
✅ Add support for **cloud storage (Google Cloud Storage, AWS S3)**  
✅ Improve **error handling & logging**  

---

## 📌 Contributing
Feel free to open issues or pull requests to improve the project!

---

🚀 **Happy Coding!** 🎯

