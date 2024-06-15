import os
from flask import Flask
from pinecone import Pinecone
from openai import OpenAI

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'  # Linux /tmp folder is used to store pdf file (testing environment) - not recommended for production environment
app.secret_key = 'replace-with-your-secret-key'    # Replace with your own secret string (testing environment) - not recommended for production environment

# Retrieve the Pinecone API key and host from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = os.getenv("PINECONE_HOST")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Error handling: Check if the environment variables are set
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set!")
if not pinecone_host:
    raise ValueError("PINECONE_HOST environment variable not set!")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# Initialize Pinecone instance
pc = Pinecone(api_key=pinecone_api_key)
index_name = "replace-with-your-pinecone-index-name"     # Pinecone index name
pinecone_index = pc.Index(index_name, host=pinecone_host)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=openai_api_key)
