from flask import Flask, request, render_template, redirect, url_for, flash, session
from config import app, pinecone_index, client
from utils import (
    extract_text_from_pdf,
    split_text_into_chunks,
    generate_embeddings,
    store_embeddings_in_pinecone,
    refine_user_query,
    generate_embedding_for_query,
    generate_response_from_chunks,
    delete_all_vectors_from_pinecone
)
from werkzeug.utils import secure_filename
import os
import numpy as np

app.config['UPLOAD_FOLDER'] = '/tmp'
app.secret_key = 'your-secret-key'

# Clear the Pinecone database at the beginning
try:
    delete_all_vectors_from_pinecone()
    print("Successfully cleared Pinecone database.")
except Exception as e:
    print(f"Error clearing Pinecone database: {e}")

@app.route("/", methods=["GET", "POST"])
def home():
    context = ""
    if 'uploaded_file' in session:
        uploaded_file = session['uploaded_file']
    else:
        uploaded_file = None

    if request.method == "POST":
        if 'end_session' in request.form:
            if uploaded_file:
                os.remove(uploaded_file)
            delete_all_vectors_from_pinecone()
            session.pop('uploaded_file', None)
            flash('Session ended and file deleted successfully.')
            return redirect(url_for('home'))

        if 'query' in request.form:
            user_query = request.form["query"]
            context = request.form["context"]
            model = request.form.get("model", "gpt-3.5-turbo")

            refined_query = refine_user_query(user_query, model)
            print(f"Refined Query: {refined_query}")

            query_embedding = generate_embedding_for_query(refined_query)
            embedding_dimension = 1536
            query_vector = np.array(query_embedding)

            if query_vector.size < embedding_dimension:
                padded_query_vector = np.pad(query_vector, (0, embedding_dimension - query_vector.size), 'constant')
            else:
                padded_query_vector = query_vector

            # Adjust and experiment the top_k value based on your use case
            results = pinecone_index.query(vector=padded_query_vector.tolist(), top_k=1, include_metadata=True)
            # Adjust the threshold value based on your use case
            score_threshold = 0.65
            filtered_matches = [match for match in results['matches'] if match['score'] > score_threshold]

            if filtered_matches:
                detailed_response = generate_response_from_chunks(filtered_matches, user_query, context, model)
            else:
                detailed_response = "No relevant results found above the threshold."

            context += f"\nUser query: {user_query}\nRefined query: {refined_query}\nResponse: {detailed_response}\n"

            return render_template("index.html", response=detailed_response, context=context, uploaded_file=uploaded_file, user_query=user_query, refined_query=refined_query, model=model, flash_message=session.pop('flash_message', None))

        elif 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Check if the file already exists and delete it if it does
                if os.path.exists(file_path):
                    os.remove(file_path)

                file.save(file_path)

                session['uploaded_file'] = file_path
                flash('File uploaded successfully.')
                return redirect(url_for('home'))

        elif 'process_file' in request.form:
            #flash('Creating embeddings and storing in the database.')
            process_file()
            flash('Created vector embeddings and stored embeddings in the database successfully.')
            return redirect(url_for('home'))

    return render_template("index.html", response="", context=context, uploaded_file=uploaded_file, user_query=None, refined_query=None, model=None, flash_message=session.pop('flash_message', None))

def process_file():
    uploaded_file = session.get('uploaded_file')
    if uploaded_file:
        text_by_page = extract_text_from_pdf(uploaded_file)
        chunks = split_text_into_chunks(text_by_page)
        embeddings = generate_embeddings(chunks)
        store_embeddings_in_pinecone(embeddings, chunks)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
