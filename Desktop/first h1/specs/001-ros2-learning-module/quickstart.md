# Quickstart

This document provides instructions on how to set up and run the Docusaurus book and the RAG chatbot.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Docker

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install frontend dependencies:**
    ```bash
    cd frontend
    npm install
    ```

3.  **Install backend dependencies:**
    ```bash
    cd ../backend
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - Create a `.env` file in the `backend` directory.
    - Add the following environment variables:
      ```
      OPENAI_API_KEY=<your-openai-api-key>
      NEON_DATABASE_URL=<your-neon-database-url>
      QDRANT_URL=<your-qdrant-url>
      ```

5.  **Start dependent services:**
    - Run Qdrant using Docker:
      ```bash
      docker run -p 6333:6333 qdrant/qdrant
      ```

## Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

2.  **Start the frontend development server:**
    ```bash
    cd frontend
    npm run start
    ```
    The Docusaurus site will be running at `http://localhost:3000`.

## Ingesting Data

To populate the vector database with the content from the Docusaurus book, run the ingestion script:

```bash
cd backend
python ingest.py
```
