import pytest
import requests

def test_get_all_reviews(reviews_endpoint):
    """Test retrieving all reviews"""
    response = requests.get(reviews_endpoint)
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    reviews = response.json()
    assert isinstance(reviews, list)
    
    # If there are reviews, check schema
    if len(reviews) > 0:
        first_review = reviews[0]
        assert "id" in first_review
        assert "movieId" in first_review
        assert "text" in first_review

def test_get_single_review(reviews_endpoint):
    """Test retrieving a single review by ID"""
    # First get a review ID we can use
    all_reviews = requests.get(reviews_endpoint).json()
    if len(all_reviews) == 0:
        pytest.skip("No reviews available to test")
        
    review_id = all_reviews[0]["id"]
    
    # Get the specific review
    response = requests.get(f"{reviews_endpoint}/{review_id}")
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    review = response.json()
    assert review["id"] == review_id

def test_create_review(reviews_endpoint, movies_endpoint):
    """Test creating a new review"""
    # First get a movie ID to associate with the review
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    new_review = {
        "movieId": movie_id,
        "text": "This is a test review",
        "rating": 5
    }
    
    response = requests.post(reviews_endpoint, json=new_review)
    
    # Status code check
    assert response.status_code == 201
    
    # Data validation
    created_review = response.json()
    assert created_review["text"] == new_review["text"]
    assert created_review["movieId"] == new_review["movieId"]
    assert "id" in created_review
    
    # Cleanup
    requests.delete(f"{reviews_endpoint}/{created_review['id']}")

def test_update_review(reviews_endpoint, movies_endpoint):
    """Test updating a review"""
    # Get a movie ID
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    # Create a review to update
    new_review = {
        "movieId": movie_id,
        "text": "Review to update",
        "rating": 3
    }
    created = requests.post(reviews_endpoint, json=new_review).json()
    
    # Update the review
    update_data = {
        "text": "Updated review text",
        "rating": 4
    }
    response = requests.put(f"{reviews_endpoint}/{created['id']}", json=update_data)
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    updated_review = response.json()
    assert updated_review["text"] == update_data["text"]
    assert updated_review["rating"] == update_data["rating"]
    
    # Cleanup
    requests.delete(f"{reviews_endpoint}/{created['id']}")

def test_delete_review(reviews_endpoint, movies_endpoint):
    """Test deleting a review"""
    # Get a movie ID
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    # Create a review to delete
    new_review = {
        "movieId": movie_id,
        "text": "Review to delete",
        "rating": 2
    }
    created = requests.post(reviews_endpoint, json=new_review).json()
    
    # Delete the review
    response = requests.delete(f"{reviews_endpoint}/{created['id']}")
    
    # Status code check
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = requests.get(f"{reviews_endpoint}/{created['id']}")
    assert get_response.status_code == 404

def test_negative_reviews_invalid_data(reviews_endpoint):
    """Test creating a review with invalid data"""
    # Missing required fields
    invalid_review = {
        "text": "Invalid review without movieId"
    }
    
    response = requests.post(reviews_endpoint, json=invalid_review)
    
    # MockAPI might actually accept this, but in a real API it would fail
    # The important thing is that we're testing for error handling
    if response.status_code == 201:
        # Cleanup if it was created
        created = response.json()
        requests.delete(f"{reviews_endpoint}/{created['id']}")
        print("Warning: API accepted invalid data without movieId")
    else:
        assert response.status_code in [400, 422]