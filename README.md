# LocalMind

## AI That Stays With You

**A privacy-first desktop AI knowledge assistant powered by local AI models.**

LocalMind enables users to build a personal knowledge base from their own documents and interact with them using locally hosted Large Language Models (LLMs). By combining Retrieval-Augmented Generation (RAG), semantic search, and offline AI processing, LocalMind delivers intelligent document insights while keeping all data securely on the user's computer.

---

## Overview

Traditional AI assistants often require users to upload sensitive documents to cloud services. LocalMind was developed to provide a secure alternative by ensuring all document processing, vector storage, and AI inference remain on the user's local machine.

Whether you're studying for an exam, researching technical material, comparing reports, or exploring large collections of documents, LocalMind helps you find answers quickly while maintaining complete privacy.

---

## Features

- 🔒 100% Local & Private AI Processing
- 📄 Upload PDF, DOCX, TXT, and Markdown documents
- 🧠 Build a searchable local knowledge base
- 💬 Ask questions about your documents
- 🔍 Semantic search using vector embeddings
- 📝 AI-generated document summaries
- 📊 Compare multiple documents
- 🎓 Generate AI-powered quizzes
- 🖥️ Cross-platform desktop application
- ⚡ FastAPI backend with streaming responses

---

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

### Desktop

- Electron

### Backend

- Python
- FastAPI

### AI & Machine Learning

- Ollama
- LangChain
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Document Processing

- PyMuPDF
- python-docx

---

## Project Structure

```text
LocalMind/
│
├── backend/
├── electron-app/
├── frontend/
├── tests/
│
├── requirements.txt
├── package.json
├── setup.bat
├── setup.sh
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/KGT13/LocalMind.git
cd LocalMind
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the project using the provided setup scripts:

**Windows**

```text
setup.bat
```

**macOS / Linux**

```text
setup.sh
```

---

## Core Capabilities

LocalMind currently supports:

- Local document ingestion
- AI-powered question answering
- Semantic document search
- AI-generated document summaries
- Document comparison
- Knowledge quizzes
- Local vector database storage
- Offline AI processing

---

## Privacy First

LocalMind was designed with privacy as its highest priority.

- Your documents remain on your computer.
- AI models run locally through Ollama.
- No cloud storage is required.
- No document data is transmitted to external services.

Your knowledge stays with you.

---

## Future Enhancements

Future versions may include:

- Voice interaction
- OCR support for scanned documents
- Flashcard generation
- Citation visualization
- Knowledge graph exploration
- Multi-user knowledge libraries

---

## Development Team

### Rolando Aedo

- Project Lead
- UI/UX Design
- Documentation
- Product Vision
- Testing

### Karell Gonzalez

- Backend Development
- AI Integration
- Electron Desktop Application
- Retrieval-Augmented Generation (RAG)

---

## Academic Project

Developed as the Capstone Project for the

**Applied Artificial Intelligence Program**

**Miami Dade College**

Summer 2026

---

## Repository

https://github.com/KGT13/LocalMind

---

## License

This project is currently being developed for educational purposes.

License to be determined.
