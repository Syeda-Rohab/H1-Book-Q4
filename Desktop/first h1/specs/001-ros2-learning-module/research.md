# Research for Docusaurus Book and RAG Chatbot

## Research Tasks

- [X] Define performance goals for chatbot response time and concurrent users.
- [X] Define initial scale for the book and expected user load for the chatbot.
- [X] Find best practices for Docusaurus project structure and deployment.
- [X] Find best practices for integrating OpenAI with a FastAPI backend for a RAG chatbot.
- [X] Find best practices for using Neon (PostgreSQL) with FastAPI.
- [X] Find best practices for using Qdrant for vector storage in a RAG application.
- [X] Research patterns for integrating a RAG chatbot into a Docusaurus website.

## Findings

### Performance Goals

*   **Chatbot Response Time:** Aim for a P95 (95th percentile) response time of under 3 seconds. The first response (acknowledgement) should be under 1 second to provide an instantaneous feel.
*   **Concurrent Users:** The system will be designed for scalability. For the initial launch, it must handle at least 10 concurrent users without performance degradation. The architecture will be built to scale horizontally to accommodate future growth.

### Initial Scale and User Load

*   **Initial Book Scale:** The book will launch with approximately 50-100 pages of content. This is a manageable size that allows for rapid iteration and ensures the Docusaurus build process remains efficient.
*   **Expected Chatbot User Load:** For a new documentation site, the initial user load is expected to be low. The chatbot will be designed to handle a baseline of 10-20 concurrent users, with the backend architecture designed for scalability (e.g., using serverless or containerized deployments) to handle future growth.

### Docusaurus Project Structure and Deployment

*   **Project Structure:**
    *   The `frontend` directory will house the Docusaurus application.
    *   `docs/`: This will contain the main content of the book, organized into subdirectories for each section.
    *   `src/pages`: This will be used for custom pages, such as the chatbot interface.
    *   `src/components`: This directory will hold custom React components for the chatbot UI and other interactive elements.
    *   `static/`: This is for images and other static assets.
    *   `docusaurus.config.js`: This file will be configured for the book's navigation, plugins, and theme.
    *   `sidebars.js`: This will define the chapter and section structure for the sidebar.
*   **Deployment:**
    *   The Docusaurus site will be deployed as a static site to Vercel for its ease of use and CI/CD integration.
    *   A GitHub Actions workflow will be created to automatically build and deploy the site to Vercel on every push to the `main` branch.
    *   The build command will be `npm run build`, and the output directory will be `build`.
    *   The production branch will be `main`.

### OpenAI and FastAPI Integration for RAG

*   **Asynchronous Endpoints:** All API endpoints in FastAPI will be defined with `async def` to handle requests concurrently and ensure non-blocking I/O.
*   **OpenAI Client:** The `AsyncOpenAI` client will be used for non-blocking calls to the OpenAI API.
*   **Dependency Injection:** FastAPI's `Depends` system will be leveraged to manage the `AsyncOpenAI` client, making the code more modular and testable.
*   **RAG Orchestration:** The `LangChain` library will be used to orchestrate the RAG pipeline, handling document loading, chunking, embedding, retrieval, and generation. This will simplify the development process and provide a robust framework.
*   **Streaming Responses:** `StreamingResponse` will be used to stream the response from the OpenAI API to the client, improving the perceived performance and user experience of the chatbot.
*   **Error Handling:** Custom exception handlers will be implemented to catch and handle potential errors from the OpenAI API or other services, providing graceful error recovery.
*   **Security:**
    *   The OpenAI API key will be stored securely in a `.env` file and loaded using `python-dotenv`.
    *   Pydantic models will be used for strict input validation to prevent malformed requests.
    *   CORS (Cross-Origin Resource Sharing) will be enabled to allow the Docusaurus frontend to communicate with the FastAPI backend.

### Neon (PostgreSQL) and FastAPI Integration

*   **Asynchronous Driver:** The `asyncpg` driver will be used for all database operations to ensure non-blocking I/O and compatibility with FastAPI's asynchronous nature.
*   **Connection Pooling:** Neon's built-in connection pooler will be leveraged. In the FastAPI application, SQLAlchemy's `NullPool` will be configured to delegate connection management entirely to Neon, which is the recommended approach for serverless databases.
*   **ORM:** `SQLAlchemy` will be used as the Object-Relational Mapper for its robust features and asynchronous support.
*   **Session Management:** A dependency injection pattern using `Depends` will be implemented to manage database sessions, ensuring that a session is created for each request and properly closed afterwards.
*   **Configuration:** The Neon database connection URL will be stored securely in a `.env` file and not hardcoded in the application.
*   **Project Structure:** The backend application will be organized into modules for database configuration, models (SQLAlchemy), schemas (Pydantic), and CRUD (Create, Read, Update, Delete) operations to maintain a clean and scalable architecture.

### Qdrant for Vector Storage in RAG

*   **Chunking Strategy:** Start with a reasonable chunk size (e.g., 512 tokens) and overlap (e.g., 64 tokens). This will be iterated upon based on evaluation results. Semantic chunking will be used where appropriate.
*   **Embedding Models:** A high-quality embedding model (e.g., from OpenAI or a leading open-source provider) will be used. Qdrant's `FastEmbed` library will be considered for efficient embedding generation.
*   **Indexing:** Qdrant's HNSW (Hierarchical Navigable Small World) index will be used for efficient similarity search. Metadata (e.g., document source, chapter) will be stored in the payload for filtering.
*   **Retrieval:** Hybrid search will be implemented, combining dense and sparse vectors for a mix of semantic and keyword search. A re-ranking model will be used to improve the relevance of the retrieved documents.
*   **Performance:** Quantization will be enabled in Qdrant to reduce memory usage and improve search speed.
*   **Deployment:** Qdrant will be run using Docker for local development, and Qdrant Cloud will be used for production to ensure a managed and scalable solution.
*   **Evaluation:** A framework like Ragas will be used to evaluate the performance of the RAG pipeline, focusing on metrics such as faithfulness, answer relevancy, and context precision.

### RAG Chatbot Integration with Docusaurus

*   **Pattern:** A custom implementation with a self-managed RAG backend will be used. This provides the most flexibility and control over the user experience and the underlying technology stack.
*   **Content Extraction:** A Python script will be developed to parse the Markdown/MDX files from the `docs/` directory, chunk the content, and generate embeddings.
*   **RAG Backend:** The FastAPI backend will serve the RAG pipeline. It will expose an API endpoint that the Docusaurus frontend can call.
*   **Frontend Integration:**
    *   A custom React component will be built for the chatbot UI.
    *   This component will be integrated into the Docusaurus site by "swizzling" the theme. The chatbot will be added to the main layout so it's accessible from all pages.
*   **Communication:** The chatbot component will communicate with the FastAPI backend using asynchronous API calls.
