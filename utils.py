import os
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import client, pinecone_index

def extract_text_from_pdf(pdf_path):
    text_by_page = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            text_by_page.append((page_num, text))
    return text_by_page

def split_text_into_chunks(text_by_page, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for page_num, text in text_by_page:
        page_chunks = splitter.split_text(text)
        for chunk in page_chunks:
            chunks.append((page_num, chunk))
    return chunks

def generate_embeddings(chunks):
    embeddings = []
    for page_num, chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"   # OpenAI text embedding model
        )
        embedding = response.data[0].embedding
        embeddings.append((page_num, embedding))
    return embeddings

def store_embeddings_in_pinecone(embeddings, chunks):
    data_points = []
    for i, ((page_num, chunk), (_, embedding)) in enumerate(zip(chunks, embeddings)):
        data_point = {
            "id": f"chunk_{i+1}",
            "values": embedding,
            "metadata": {"text": chunk, "page_num": page_num}
        }
        data_points.append(data_point)

    pinecone_index.upsert(data_points)
    print(f"Successfully stored {len(data_points)} data points in Pinecone")

def refine_user_query(user_query, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI assistant that refines user queries for better search results."},
            {"role": "user", "content": f"Refine the following query for better search results: '{user_query}'"}
        ],
        max_tokens=50
    )
    return response.choices[0].message.content

def generate_embedding_for_query(query):
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding

def generate_response_from_chunks(chunks, user_query, context, model):
    combined_texts = []
    for chunk in chunks:
        text = chunk['metadata']['text']
        page_num = chunk['metadata'].get('page_num', 'Unknown')
        combined_texts.append(f"<p><strong>(Page {page_num + 1}):</strong> {text}</p>")

    combined_text = "\n".join(combined_texts)

    prompt = (
        f"You are an AI assistant. Based on the following information and the previous context, "
        f"provide a detailed and accurate response to the user's query: '{user_query}'. "
        f"Include the page numbers where the information was found. Only use the information provided below "
        f"and do not include any additional details that are not mentioned in the text.\n\n"
        f"Previous context:\n{context}\n\n"
        f"Here is the relevant information:\n\n{combined_text}\n\n"
        f"Please make sure to include the page numbers in your response.\n\nResponse:"
    )

    print(f"DEBUG: Prompt being sent to OpenAI:\n{prompt}\n")

    response = client.chat.completions.create(                 # openai.ChatCompletion.create method can be used as well - currently testing
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI assistant providing detailed responses based on given texts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def delete_all_vectors_from_pinecone():
    try:
        pinecone_index.delete(delete_all=True)
        print("Successfully deleted all vectors in the index")
    except Exception as e:
        print(f"Error deleting vectors from Pinecone: {e}")
