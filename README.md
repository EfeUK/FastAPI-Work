# FastAPI

This project is to check that the application runs in a RESTful manner.
An API spec document will be created include an update to the application code.

User accounts will be created with information on name, description, balance and a boolean to state if the account is active.

# Overview

- empty __init__.py 
- main.py (The full and complete code of the FastAPI)
    - import types
    - Classes
    -  async def method definitions 
    - @app HTTP get and request methods
        - get account
        - post account
        - put, to update the account fully 
        - patch - to update specific attributes 
        - delete, to delete an account
    - Dockerfile to place the entire work on an image container
    - git - to specify code and its results on GitHub.

The API will perform with memory in session to show full functionality.

View the full API via

http://127.0.0.1/docs