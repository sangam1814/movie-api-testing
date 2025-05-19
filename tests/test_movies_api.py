import pytest
import requests

def test_get_all_movies(movies_endpoint):
    """Test retrieving all movies"""
    response = requests.get(movies_endpoint)
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    movies = response.json()
    assert isinstance(movies, list)
    assert len(movies) > 0
    
    # Schema validation for first movie
    first_movie = movies[0]
    assert "id" in first_movie
    assert "name" in first_movie

def test_get_single_movie(movies_endpoint):
    """Test retrieving a single movie by ID"""
    # First get a movie ID we can use
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    # Get the specific movie
    response = requests.get(f"{movies_endpoint}/{movie_id}")
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    movie = response.json()
    assert movie["id"] == movie_id

def test_create_movie(movies_endpoint):
    """Test creating a new movie"""
    new_movie = {
        "name": "Test Movie",
        "genre": "Action",
        "releaseYear": 2023
    }
    
    response = requests.post(movies_endpoint, json=new_movie)
    
    # Status code check
    assert response.status_code == 201
    
    # Data validation
    created_movie = response.json()
    assert created_movie["name"] == new_movie["name"]
    assert created_movie["genre"] == new_movie["genre"]
    assert "id" in created_movie
    
    # Cleanup - delete the created movie
    requests.delete(f"{movies_endpoint}/{created_movie['id']}")

def test_update_movie(movies_endpoint):
    """Test updating a movie"""
    # Create a movie to update
    new_movie = {
        "name": "Movie to Update",
        "genre": "Comedy",
        "releaseYear": 2022
    }
    created = requests.post(movies_endpoint, json=new_movie).json()
    
    # Update the movie
    update_data = {
        "name": "Updated Movie Title",
        "genre": "Drama"
    }
    response = requests.put(f"{movies_endpoint}/{created['id']}", json=update_data)
    
    # Status code check
    assert response.status_code == 200
    
    # Data validation
    updated_movie = response.json()
    assert updated_movie["name"] == update_data["name"]
    assert updated_movie["genre"] == update_data["genre"]
    
    # Cleanup
    requests.delete(f"{movies_endpoint}/{created['id']}")

def test_delete_movie(movies_endpoint):
    """Test deleting a movie"""
    # Create a movie to delete
    new_movie = {
        "name": "Movie to Delete",
        "genre": "Horror"
    }
    created = requests.post(movies_endpoint, json=new_movie).json()
    
    # Delete the movie
    response = requests.delete(f"{movies_endpoint}/{created['id']}")
    
    # Status code check
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = requests.get(f"{movies_endpoint}/{created['id']}")
    assert get_response.status_code == 404

def test_negative_get_nonexistent_movie(movies_endpoint):
    """Test getting a movie with a non-existent ID"""
    response = requests.get(f"{movies_endpoint}/99999")
    assert response.status_code == 404