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

The requirements.txt file lists the necessary Python packages and their versions required to run the application. Here's a breakdown of each package:

**flask**: A lightweight Python web framework for building web applications.

**pinecone-client**: The official Python client library for interacting with Pinecone, the vector database used in your application.

**openai**: The official Python client library for the OpenAI API, used to generate text embeddings and interact with OpenAI's language models.

**pypdf2**: A pure-python library for extracting text from PDF files.

**langchain**: A framework for building applications with large language models, used in your application for text splitting and chunking.

**numpy**: A package for scientific computing in Python, used for working with multidimensional arrays and vectors.

To install these dependencies, you can create a new python virtual environment and run the following command:

pip install -r requirements.txt

# API integration

For integrating with OpenAI and Pinecone, you need to obtain and configure the respective API keys, host (pinecone) information for these platforms. Set your OpenAI and Pinecone API keys, and Pinecone host as environment variables in Linux. Use the following Linux commands to export these variables:

export OPENAI_API_KEY='your-openai-api-key'

export PINECONE_API_KEY='your-pinecone-api-key'

export PINECONE_HOST='your-pinecone-host'

Ensure you have an OpenAI account with valid API keys. You can obtain your API keys from the OpenAI platform (https://platform.openai.com/) and manage them (https://platform.openai.com/organization/api-keys). Additionally, ensure that your account has sufficient usage quota, as this example requires a paid OpenAI account.

Pinecone environment (Pinecone free account used https://www.pinecone.io/): 1) Pinecone Index is used 2) Dimensions: 1536 3) Host type: Serverless.

CentOS Linux release 8.5.2111 is used as Linux OS. Create a python virtual environment (optional but recommended) to isolate project dependencies.
