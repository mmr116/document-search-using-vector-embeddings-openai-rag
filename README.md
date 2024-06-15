# An application to generate vector embeddings for PDF document, store them in a vector database, and enable semantic search and information retrieval using OpenAI's language models.

This project provides a simple web application that enables users to upload a PDF document, generate vector embeddings from its content, and then search for information within the document using a text query. OpenAI's embedding and language models are used for creating vector embeddings and information retrieval.

# Key features

**PDF document ingestion**: Users can upload PDF document through the web interface for information retrieval.

**Generate vector embeddings**: Text content is extracted from the PDF and split into smaller chunks using Langchain. Embeddings are generated for each chunk using OpenAI's text embedding model (e.g., text-embedding-ada-002).

**Vector Database Storage**: Store the generated vector embeddings in a vector database like Pinecone for similarity search.

**Refine user queries**: User queries are refined using OpenAI's chat completion API to improve search accuracy.

**Search for information**: Users can enter text queries to search for information within the uploaded document. The system retrieves relevant text chunks based on their vector similarity to the query embedding.

**Generate response**: Based on the retrieved text chunks, context (previous queries and responses), and the user's query, a response is generated using OpenAI models (gpt-4o, gpt-4, or gpt-3.5-turbo). Users can select the OpenAI model through the web interface. The choice of model can affect the response style, detail, and accuracy.

# Required packages

The requirements.txt file lists the necessary Python packages and their versions required to run the application. Here's a breakdown of each package:

**flask**: A lightweight Python web framework for building web applications.

**pinecone-client**: The official Python client library for interacting with Pinecone, the vector database used in your application.

**openai**: The official Python client library for the OpenAI API, used to generate text embeddings and interact with OpenAI's language models.

**pypdf2**: A pure-python library for extracting text from PDF files.

**langchain**: A framework for building applications with large language models, used in your application for text splitting and chunking.

**numpy**: A package for scientific computing in Python, used for working with multidimensional arrays and vectors.

To install these dependencies, you can create a new python virtual environment and run the following command:

pip install -r requirements.txt

# API integration and environment

For integrating with OpenAI and Pinecone, you need to obtain and configure the respective API keys, host (pinecone) information for these platforms. Set your OpenAI and Pinecone API keys, and Pinecone host as environment variables in Linux. Use the following Linux commands to export these variables:

export OPENAI_API_KEY='your-openai-api-key'

export PINECONE_API_KEY='your-pinecone-api-key'

export PINECONE_HOST='your-pinecone-host'

Ensure you have an OpenAI account with valid API keys. You can create or obtain your API keys from the OpenAI platform (https://platform.openai.com/) and manage them (https://platform.openai.com/organization/api-keys). Additionally, ensure that your account has sufficient usage quota, as this example requires a paid OpenAI account.

Pinecone environment (Pinecone free account used https://www.pinecone.io/): 1) Pinecone Index is used 2) Dimensions: 1536 3) Host type: Serverless.

CentOS Linux release 8.5.2111 is used as Linux OS. A cloud Linux VM with a public IP (optional) has been tested for web interface. Local IP can be used as well. Create a python virtual environment (optional but recommended) to isolate project dependencies.

# How it works

The application provides a web interface built with Flask, a Python web framework. Users can upload PDF document, enter queries, choose the OpenAI language model to use (GPT-3.5-turbo, GPT-4, or GPT-4o), and receive detailed responses based on the information extracted from the uploaded PDF documents.

**Ingesting PDF document and creating vector embeddings**

The application provides a web interface where users can upload PDF documents. Upon uploading a PDF file, the text content is extracted from the document and split into smaller chunks using the RecursiveCharacterTextSplitter from the LangChain library. This splitting process ensures that the text is divided into manageable chunks while maintaining context.

Next, vector embeddings are generated for each text chunk using OpenAI's text-embedding-ada-002 model. These embeddings are high-dimensional vectors that capture the semantic meaning of the text, enabling efficient similarity search.

**Storing vector embeddings in Pinecone**

The generated vector embeddings, along with their corresponding text chunks and page numbers, are stored in a Pinecone vector database. Pinecone is a scalable and efficient vector database designed for storing and querying high-dimensional vectors.

**Query Processing**

When a user submits a query through the web interface, the application processes it in the following steps:

- Query Refinement:

  The user's query is sent to OpenAI's language model (e.g., GPT-3.5-turbo, GPT-4, or GPT-4o) to refine and improve the query for better search accuracy.

- Embedding generation for the query

  The refined query is converted into a vector embedding using OpenAI's text-embedding-ada-002 model.

- Similarity search:

  The query embedding is used to search the Pinecone vector database for the most semantically similar text chunks based on vector similarity.

- Response generation:

  The relevant text chunks retrieved from the database are combined with the previous context (if any) and the original user query. This information is then sent to OpenAI's language model (the same model used for query refinement) to generate a comprehensive and contextually relevant response.

- Context aware response:

  The application maintains a context of previous queries and responses. This context is passed to OpenAI's language model during the response generation step, ensuring that the generated responses take into account the conversational history and provide accurate and contextually relevant information.

  
  
