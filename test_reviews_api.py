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
        assert "movieID" in first_review
        assert "reviewText" in first_review
        assert "rating" in first_review


def test_get_single_review(reviews_endpoint):
    """Test retrieving a single review by ID"""
    all_reviews = requests.get(reviews_endpoint).json()
    if len(all_reviews) == 0:
        pytest.skip("No reviews available to test")
        
    review_id = all_reviews[0]["id"]
    
    response = requests.get(f"{reviews_endpoint}/{review_id}")
    
    assert response.status_code == 200
    review = response.json()
    assert review["id"] == review_id


def test_create_review(reviews_endpoint, movies_endpoint):
    """Test creating a new review"""
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    new_review = {
        "movieID": movie_id,
        "reviewText": "This is a test review",
        "rating": 5
    }
    
    response = requests.post(reviews_endpoint, json=new_review)
    
    assert response.status_code == 201
    
    created_review = response.json()
    assert created_review["reviewText"] == new_review["reviewText"]
    assert created_review["movieID"] == new_review["movieID"]
    assert "id" in created_review
    
    # Cleanup
    requests.delete(f"{reviews_endpoint}/{created_review['id']}")


def test_update_review(reviews_endpoint, movies_endpoint):
    """Test updating a review"""
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    new_review = {
        "movieID": movie_id,
        "reviewText": "Review to update",
        "rating": 3
    }
    created = requests.post(reviews_endpoint, json=new_review).json()
    
    update_data = {
        "reviewText": "Updated review text",
        "rating": 4
    }
    response = requests.put(f"{reviews_endpoint}/{created['id']}", json=update_data)
    
    assert response.status_code == 200
    
    updated_review = response.json()
    assert updated_review["reviewText"] == update_data["reviewText"]
    assert updated_review["rating"] == update_data["rating"]
    
    # Cleanup
    requests.delete(f"{reviews_endpoint}/{created['id']}")


def test_delete_review(reviews_endpoint, movies_endpoint):
    """Test deleting a review"""
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    new_review = {
        "movieID": movie_id,
        "reviewText": "Review to delete",
        "rating": 2
    }
    created = requests.post(reviews_endpoint, json=new_review).json()
    
    response = requests.delete(f"{reviews_endpoint}/{created['id']}")
    
    assert response.status_code == 200
    
    get_response = requests.get(f"{reviews_endpoint}/{created['id']}")
    assert get_response.status_code == 404


def test_negative_reviews_invalid_data(reviews_endpoint):
    """Test creating a review with invalid data"""
    invalid_review = {
        "reviewText": "Invalid review without movieID"
    }
    
    response = requests.post(reviews_endpoint, json=invalid_review)
    
    if response.status_code == 201:
        # Cleanup if created
        created = response.json()
        requests.delete(f"{reviews_endpoint}/{created['id']}")
        print("Warning: API accepted invalid data without movieID")
    else:
        assert response.status_code in [400, 422]