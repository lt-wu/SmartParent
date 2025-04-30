import faiss
import numpy as np
import json
import os
from tools.refineRes import refineRes

from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

# Environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")

EMBEDDING_DIMENSION = 512

# Global variable for FAISS index
faiss_index = None


def save_to_db():
    """
    Save the summarized JSON response (`json_res`) into a FAISS database.

    This function converts the JSON data into embeddings (e.g., using OpenAI embeddings or similar)
    and stores them in a FAISS index for efficient retrieval.

    Returns:
        str: Status message indicating success or failure.
    """
    global json_res, faiss_index
    json_res =  {'data': [{'subject': 'Earth Day', 'start_date': '2025-04-22T00:00:00', 'end_date': '2025-04-22T23:59:59', 'description': 'Earth Day event to celebrate environmental awareness'}, {'subject': 'ABC Countdown Begins', 'start_date': '2025-04-28T00:00:00', 'end_date': '2025-04-28T23:59:59', 'description': 'The start of the ABC Countdown, more info coming soon'}, {'subject': 'Art Show', 'start_date': '2025-04-28T17:00:00', 'end_date': '2025-04-28T20:00:00', 'description': 'Art Show event showcasing student artworks'}, {'subject': 'Talent Show Submissions Due', 'start_date': '2025-05-01T00:00:00', 'end_date': '2025-05-01T23:59:59', 'description': 'Deadline for Talent Show submissions'}, {'subject': 'STEAM Day', 'start_date': '2025-05-02T00:00:00', 'end_date': '2025-05-02T23:59:59', 'description': 'STEAM Day event, more info coming soon'}, {'subject': 'Teacher Appreciation Week', 'start_date': '2025-05-05T00:00:00', 'end_date': '2025-05-09T23:59:59', 'description': 'Week dedicated to appreciating teachers'}, {'subject': 'Frozen Jr. Drama Performance', 'start_date': '2025-05-08T00:00:00', 'end_date': '2025-05-08T23:59:59', 'description': 'Drama performance of Frozen Jr, more info coming soon'}, {'subject': 'Last Day of After School Clubs', 'start_date': '2025-05-15T00:00:00', 'end_date': '2025-05-15T23:59:59', 'description': 'Final day for after school clubs'}, {'subject': 'No Clubs', 'start_date': '2025-05-19T00:00:00', 'end_date': '2025-05-23T23:59:59', 'description': 'Period with no clubs scheduled'}, {'subject': 'Spring Talent Shows', 'start_date': '2025-05-19T00:00:00', 'end_date': '2025-05-19T23:59:59', 'description': 'Spring Talent Shows event'}, {'subject': 'Last Blast Celebration', 'start_date': '2025-05-21T00:00:00', 'end_date': '2025-05-21T23:59:59', 'description': 'Last Blast Celebration, more info coming soon'}, {'subject': '1st-4th Grade Ceremonies', 'start_date': '2025-05-23T00:00:00', 'end_date': '2025-05-23T23:59:59'}]}

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

def add_text_to_faiss_db(file_path):
    """
    Add a new text file's content to the FAISS database.

    Args:
        file_path (str): Path to the text file to be added.

    Returns:
        str: Status message indicating success or failure.
    """
    global faiss_index, metadata_store

    # Load text content from the file
    try:
        with open(file_path, 'r') as f:
            text_content = f.read()
        print(f"Loaded content from {file_path}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")

    # Generate embedding for the text content (replace with actual embedding logic)
    # Example: Mock embedding creation
    text_embedding = np.random.rand(EMBEDDING_DIMENSION).astype('float32')  # Dummy embedding

    # Initialize FAISS index if not already done
    if faiss_index is None:
        faiss_index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)  # L2 distance index
        print("Initialized FAISS index.")

    # Add embedding to FAISS index
    faiss_index.add(np.array([text_embedding]))  # Add single embedding (reshape if necessary)

    # Update metadata store with file information
    metadata_store.append({
        "file_path": file_path,
        "content": text_content,
        "embedding": text_embedding.tolist()  # Optional: Store embedding for debugging
    })

    print(f"Added text file '{file_path}' to FAISS database.")
    return f"Successfully added '{file_path}' to FAISS database."

def query_faiss_db(faiss_index, metadata_store, query_embedding):
    """
    Query the FAISS database for similar events based on a given embedding.

    Args:
        query_embedding (np.array): The embedding of the query.

    Returns:
        List[Dict]: List of matching events from FAISS database.
    """

    if faiss_index is None:
        raise ValueError("FAISS database has not been initialized. Run 'save_to_faiss_db' first.")

    if not isinstance(query_embedding, np.ndarray):
        raise ValueError("Invalid query embedding. Must be a NumPy array.")

    # Perform similarity search
    k = 5  # Number of nearest neighbors to retrieve
    distances, indices = faiss_index.search(query_embedding.reshape(1, -1), 10)

    # Retrieve events based on indices
    matching_events = [metadata_store[i] for i in indices[0] if i < len(metadata_store)]
    print("Matching events:", matching_events)

    return matching_events


# Example function to generate a query embedding (replace with actual embedding logic)
def generate_query_embedding(query_text):
    """
    Generate an embedding for the given query text.

    Args:
        query_text (str): The text to generate the embedding for.

    Returns:
        np.array: Generated embedding.
    """
    embedding_dimension = 512
    return np.random.rand(embedding_dimension).astype('float32')  # Dummy embedding


def rewrite_query_based_on_results(query_text, results):
    """
    Use GPT-4o to rewrite the query based on the results retrieved from the FAISS database.

    Args:
        query_text (str): The original query text.
        results (List[Dict]): The list of matching events retrieved from the FAISS database.

    Returns:
        str: The refined query rewritten by GPT-4o.
    """
    if not results:
        return query_text  # If no results, return the original query

    # Generate the refined query using GPT-4o
    response = refineRes(api_key, query_text, results)
    return response.strip() if response else query_text  # Handle empty or invalid responses



# # Example usage
# if __name__ == "__main__":
#     # Save data to FAISS database
#     save_to_faiss_db()

#     # Query FAISS database
#     query_text = "which day is Art Show?"
#     query_embedding = generate_query_embedding(query_text)
#     results = query_faiss_db(query_embedding)
#     print("Query results:", results)

#     # Rewrite query based on results
#     refined_query = rewrite_query_based_on_results(query_text, results)
#     print("Refined Query:", refined_query)