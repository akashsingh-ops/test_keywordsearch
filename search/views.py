from django.http import JsonResponse
from sentence_transformers import SentenceTransformer
import chromadb
from .models import KeywordData  # If you are using models
  # Direct import
from django.views.decorators.csrf import csrf_exempt
import uuid
from data import keyword_data  # Adjusted to use relative import

# Initialize ChromaDB Client
client = chromadb.Client()

# Initialize Sentence Transformer model for vectorization
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Vectorize and upload data to ChromaDB

@csrf_exempt
def upload_data(request):
    collection = client.create_collection("keywords")

    # Loop through keyword data and create vectors
    for data in keyword_data:
        combined_text = f"{data['Category']} {data['Topic']} {data['Term']} {data['Variable_Level_1']}"

        vector = model.encode(combined_text)

        # Generate a unique ID for each entry
        unique_id = str(uuid.uuid4())

        # Store vectorized data in ChromaDB
        collection.add(
            documents=[combined_text],
            embeddings=[vector.tolist()],
            metadatas=[data],
            ids=[unique_id]  # Provide unique ID
        )
        print(collection)

    
    return JsonResponse({'status': 'Data uploaded successfully'})

def keyword_suggestion(request):
    keyword = request.GET.get('keyword', '')
    
    # Check if the keyword is provided
    if not keyword:
        return JsonResponse({'suggestions': []})  # Return empty suggestions if no keyword

    # Get the collection named "keywords"
    collection = client.get_collection("keywords")

    # Search for keywords based on the user input
    try:
        results = collection.query(
            query_embeddings=[model.encode(keyword).tolist()],  # Vectorize the keyword
            n_results=10  # Number of results to return
        )
    except Exception as e:
        print("Error querying ChromaDB:", e)
        return JsonResponse({'suggestions': []})  # Return empty suggestions on error

    # Log the results for debugging
    print("Results from ChromaDB:", results)

    # Check if 'results' is in the response and contains data
    suggestions = []
    if 'results' in results and results['results']:
        suggestions = [result['document'] for result in results['results'][0]]

    return JsonResponse({'suggestions': suggestions})
    