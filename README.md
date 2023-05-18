# 449 Final Project

## CPSC 449 Sec 02 Class Number 13992 Spring 2023

## Developers: Nicholas Caro, Justin Kim, Andrew Jung

### How To Run Via Terminal

1. Cd to the project directory `cd /path/to/project`
2. Activate the environment `source bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Run uviorn server `uvicorn main:app --reload`

### How to Access API Schema While Uvicorn Server is Running
1. Go on web browser and go to `http://127.0.0.1:8000/redoc`
2. API Schema will display and describe each API endpoint
3. Test API endpoint using Postman

### Design Choices and Implementation
1. uvicorn for server to see FastAPI
2. FastAPI to implement APIs
3. Pydantic models for data models and data validation
4. MongoDB for database
5. PyMongo to establish connection with MongoDB
6. Async for asynchronous connection

