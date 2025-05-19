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
    assert "title" in first_movie  # FIXED here

def test_get_single_movie(movies_endpoint):
    """Test retrieving a single movie by ID"""
    all_movies = requests.get(movies_endpoint).json()
    movie_id = all_movies[0]["id"]
    
    response = requests.get(f"{movies_endpoint}/{movie_id}")
    assert response.status_code == 200
    
    movie = response.json()
    assert movie["id"] == movie_id

def test_create_movie(movies_endpoint):
    """Test creating a new movie"""
    new_movie = {
        "title": "Test Movie",  # FIXED here
        "genre": "Action",
        "releaseYear": 2023
    }
    
    response = requests.post(movies_endpoint, json=new_movie)
    assert response.status_code == 201
    
    created_movie = response.json()
    assert created_movie["title"] == new_movie["title"]  # FIXED here
    assert created_movie["genre"] == new_movie["genre"]
    assert "id" in created_movie
    
    requests.delete(f"{movies_endpoint}/{created_movie['id']}")

def test_update_movie(movies_endpoint):
    """Test updating a movie"""
    new_movie = {
        "title": "Movie to Update",  # FIXED here
        "genre": "Comedy",
        "releaseYear": 2022
    }
    created = requests.post(movies_endpoint, json=new_movie).json()
    
    update_data = {
        "title": "Updated Movie Title",  # FIXED here
        "genre": "Drama"
    }
    response = requests.put(f"{movies_endpoint}/{created['id']}", json=update_data)
    assert response.status_code == 200
    
    updated_movie = response.json()
    assert updated_movie["title"] == update_data["title"]  # FIXED here
    assert updated_movie["genre"] == update_data["genre"]
    
    requests.delete(f"{movies_endpoint}/{created['id']}")

def test_delete_movie(movies_endpoint):
    """Test deleting a movie"""
    new_movie = {
        "title": "Movie to Delete",  # FIXED here
        "genre": "Horror"
    }
    created = requests.post(movies_endpoint, json=new_movie).json()
    
    response = requests.delete(f"{movies_endpoint}/{created['id']}")
    assert response.status_code == 200
    
    get_response = requests.get(f"{movies_endpoint}/{created['id']}")
    assert get_response.status_code == 404

def test_negative_get_nonexistent_movie(movies_endpoint):
    """Test getting a movie with a non-existent ID"""
    response = requests.get(f"{movies_endpoint}/99999")
    assert response.status_code == 404