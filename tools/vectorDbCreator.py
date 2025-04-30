
from PIL import Image
import json
import os
import re
import faiss
import numpy as np

# Global variable for FAISS index
faiss_index = None

def vectorDbCreator():
    """
    Save the summarized JSON response (`json_res`) into a FAISS database.

    This function converts the JSON data into embeddings (e.g., using OpenAI embeddings or similar)
    and stores them in a FAISS index for efficient retrieval.

    Returns:
        str: Status message indicating success or failure.
    """
    global json_res, faiss_index

    # Ensure `pairedDataSummarizer` has been executed and data is available
    if json_res is None:
        raise ValueError("No summarized data available. Run 'pairedDataSummarizer' first.")

    # Convert JSON response to embeddings (e.g., using a hypothetical embedding function)
    try:
        parsed_json = json.loads(json_res) if isinstance(json_res, str) else json_res
        print(f"Parsed JSON: {parsed_json}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        raise ValueError(f"Invalid JSON format: {json_res}")

    if "data" not in parsed_json:
        raise ValueError("'data' key not found in the JSON response.")

    # Example embedding generation (replace this with actual embedding logic)
    embedding_dimension = 512  # Example dimension for embeddings
    event_embeddings = []
    event_metadata = []

    for event in parsed_json["data"]:
        # Mock embedding creation: Replace with actual embedding generation logic
        event_embedding = np.random.rand(embedding_dimension).astype('float32')  # Dummy embedding
        event_embeddings.append(event_embedding)
        event_metadata.append(event)

    # Initialize FAISS index if not already done
    if faiss_index is None:
        faiss_index = faiss.IndexFlatL2(embedding_dimension)  # L2 distance index
        print("Initialized FAISS index.")

    # Add embeddings to FAISS index
    faiss_index.add(np.array(event_embeddings))

    # Optionally, store metadata separately (e.g., using a dictionary or database)
    global metadata_store
    metadata_store = event_metadata

    print("FAISS database updated with event embeddings.")
    return "FAISS database updated successfully."
