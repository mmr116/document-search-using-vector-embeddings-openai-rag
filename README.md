# An application to generate vector embeddings for PDF document, store them in a vector database, and enable semantic search and information retrieval using OpenAI's language models.

This project provides a simple web application that enables users to upload a PDF document, generate vector embeddings from its content, and then search for information within the document using a text query. OpenAI's embedding and language models are used for creating vector embeddings and information retrieval.

# Key features

**PDF document ingestion**: Users can upload PDF document through the web interface for information retrieval.

**Generate vector embeddings**: Text content is extracted from the PDF and split into smaller chunks using Langchain. Embeddings are generated for each chunk using OpenAI's text embedding model (e.g., text-embedding-ada-002).

**Vector Database Storage**: Store the generated vector embeddings in a vector database like Pinecone for similarity search.

**Refine user queries**: User queries are refined using OpenAI's chat completion API to improve search accuracy.

**Search for information**: Users can enter text queries to search for information within the uploaded document. The system retrieves relevant text chunks based on their vector similarity to the query embedding.

**Generate response**: Based on the retrieved text chunks, context (previous queries and responses), and the user's query, a response is generated using OpenAI models (gpt-4o, gpt-4, or gpt-3.5-turbo). Users can select the OpenAI model through the web interface. The choice of model can affect the response style, detail, and accuracy.

# Requirements
