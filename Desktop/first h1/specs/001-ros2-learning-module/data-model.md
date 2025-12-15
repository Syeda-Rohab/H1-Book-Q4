# Data Model

This document outlines the key data entities for the Docusaurus book and the RAG chatbot.

## Book Entities

### Learning Module
Represents the entire educational unit.
- **Fields**:
    - `id`: Unique identifier for the module.
    - `title`: The title of the module.
    - `description`: A brief description of the module.
- **Relationships**:
    - Has many `Chapter`s.

### Chapter
A distinct section of the module focusing on a specific topic.
- **Fields**:
    - `id`: Unique identifier for the chapter.
    - `title`: The title of the chapter.
    - `content`: The full content of the chapter in Markdown format.
    - `module_id`: Foreign key to the `Learning Module`.
- **Relationships**:
    - Belongs to one `Learning Module`.
    - Has many `Code Example`s.

### Code Example
A snippet of code demonstrating a concept.
- **Fields**:
    - `id`: Unique identifier for the code example.
    - `language`: The programming language of the code snippet.
    - `code`: The code itself.
    - `chapter_id`: Foreign key to the `Chapter`.
- **Relationships**:
    - Belongs to one `Chapter`.

### URDF Model
A file that specifies the structure of a robot model.
- **Fields**:
    - `id`: Unique identifier for the URDF model.
    - `name`: The name of the model.
    - `content`: The XML content of the URDF file.
    - `chapter_id`: Foreign key to the `Chapter`.
- **Relationships**:
    - Belongs to one `Chapter`.

## Chatbot Entities

### User
A user interacting with the chatbot.
- **Fields**:
    - `id`: Unique identifier for the user.
    - `created_at`: Timestamp of when the user was created.

### Conversation
A series of messages between a user and the chatbot.
- **Fields**:
    - `id`: Unique identifier for the conversation.
    - `user_id`: Foreign key to the `User`.
    - `created_at`: Timestamp of when the conversation started.
- **Relationships**:
    - Belongs to one `User`.
    - Has many `Message`s.

### Message
A single message in a conversation.
- **Fields**:
    - `id`: Unique identifier for the message.
    - `conversation_id`: Foreign key to the `Conversation`.
    - `role`: The role of the message sender ('user' or 'assistant').
    - `content`: The text of the message.
    - `created_at`: Timestamp of when the message was created.
- **Relationships**:
    - Belongs to one `Conversation`.

### Document
A single document in the Docusaurus book, used for the RAG pipeline.
- **Fields**:
    - `id`: Unique identifier for the document.
    - `source`: The URL or file path of the document.
    - `content`: The full content of the document.

### Chunk
A smaller piece of a document, used for retrieval.
- **Fields**:
    - `id`: Unique identifier for the chunk.
    - `document_id`: Foreign key to the `Document`.
    - `content`: The text of the chunk.
    - `vector`: The embedding vector of the chunk.
- **Relationships**:
    - Belongs to one `Document`.
