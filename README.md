# Movie API Testing Project

A comprehensive test suite for a movie database API using Python, pytest, and the requests library. This project demonstrates automated testing of RESTful APIs, focusing on CRUD operations for movies and reviews.

## Project Overview

This project showcases:
- API testing fundamentals
- Test automation with pytest
- RESTful API concepts
- Continuous Integration setup with GitHub Actions

## API Under Test

The project tests a mock API with the following endpoints:
- `/movies` - Movie resources with CRUD operations
- `/reviews` - Review resources with CRUD operations

Base URL: `https://682ad119ab2b5004cb37d298.mockapi.io/`

## Test Coverage

### Movies API:
- ✅ Get all movies
- ✅ Get a specific movie
- ✅ Create a new movie
- ✅ Update an existing movie
- ✅ Delete a movie
- ✅ Error handling for non-existent resources

### Reviews API:
- ✅ Get all reviews
- ✅ Get a specific review
- ✅ Create a new review
- ✅ Update an existing review
- ✅ Delete a review
- ✅ Error handling for invalid data

## Project Structure