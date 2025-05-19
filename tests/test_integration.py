import pytest
import requests

def test_create_movie_with_review(movies_endpoint, reviews_endpoint):
    """Test creating a movie and then adding a review to it"""
    # Step 1: Create a movie
    new_movie = {
        "name": "Integration Test Movie",
        "genre": "Sci-Fi",
        "releaseYear": 2023
    }
    
    movie_response = requests.post(movies_endpoint, json=new_movie)
    assert movie_response.status_code == 201
    
    created_movie = movie_response.json()
    movie_id = created_movie["id"]
    
    # Step 2: Create a review for that movie
    new_review = {
        "movieId": movie_id,
        "text": "This is a review for the integration test movie",
        "rating": 5
    }
    
    review_response = requests.post(reviews_endpoint, json=new_review)
    assert review_response.status_code == 201
    
    created_review = review_response.json()
    review_id = created_review["id"]
    
    # Step 3: Verify the review is associated with the movie
    assert created_review["movieId"] == movie_id
    
    # Step 4: Clean up - Delete the review and movie
    requests.delete(f"{reviews_endpoint}/{review_id}")
    requests.delete(f"{movies_endpoint}/{movie_id}")

def test_movie_lifecycle(movies_endpoint):
    """Test the complete lifecycle of a movie resource"""
    # Create
    new_movie = {
        "name": "Lifecycle Test Movie",
        "genre": "Drama",
        "releaseYear": 2024
    }
    
    create_response = requests.post(movies_endpoint, json=new_movie)
    assert create_response.status_code == 201
    
    created_movie = create_response.json()
    movie_id = created_movie["id"]
    
    # Read
    read_response = requests.get(f"{movies_endpoint}/{movie_id}")
    assert read_response.status_code == 200
    assert read_response.json()["name"] == new_movie["name"]
    
    # Update
    update_data = {
        "name": "Updated Lifecycle Movie",
        "genre": "Comedy"
    }
    
    update_response = requests.put(f"{movies_endpoint}/{movie_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == update_data["name"]
    
    # Delete
    delete_response = requests.delete(f"{movies_endpoint}/{movie_id}")
    assert delete_response.status_code == 200
    
    # Verify deletion
    verify_response = requests.get(f"{movies_endpoint}/{movie_id}")
    assert verify_response.status_code == 404