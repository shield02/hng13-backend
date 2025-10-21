# Backend - Stage 1 Task

## Task - String Analyzer Program Endpoint

In this task, I build a simple RESTFul API endpoint that
service that analyzes strings and stores their computed 
properties.

For each analyzed string, the following properties are computed and store:
- `length`: Number of characters in the string
- `is_palindrome`: Boolean indicating if the string reads the same forwards and backwards (case-insensitive)
- `unique_characters`: Count of distinct characters in the string
- `word_count`: Number of words separated by whitespace
- `sha256_hash`: SHA-256 hash of the string for unique identification
- `character_frequency_map`: Object/dictionary mapping each character to its occurrence count

The endpoints:
- `/strings`: \[POST\] Create/Analyze String, Content-Type: application/json
  Request Body:
  `
      {
      "value": "string to analyze"
      }
  `

  Success Response (201 Created):
`
  {
    "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
  "length": 16,
  "is_palindrome": false,
  "unique_characters": 12,
  "word_count": 3,
  "sha256_hash": "abc123...",
  "character_frequency_map": {
  "s": 2,
  "t": 3,
  "r": 2,
  // ... etc
  }
  },
  "created_at": "2025-08-27T10:00:00Z"
  }
`


- `/strings/{string_value}`: \[GET\] Get Specific String

- `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a`: \[GET\] Get All Strings 
  with Filtering

- `/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`: \[GET\] Natural Language 
  Filtering

- `/strings/{string_value}`: \[DELETE\] Delete String

## How to Run the App Locally

`make setup`: create venv, install deps, create .env

`make run`: start Flask app

`make test`: run all tests in /test

`make deploy` push to Heroku and open app in default browser

`make clean`: cleanup things
