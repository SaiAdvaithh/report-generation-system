''' from fastapi import FastAPI
from app.controllers import report_controller

app = FastAPI()

#registers all the routes inside the controller
app.include_router(report_controller.router) 

@app.get("/")
def home():
    return {"message": "Report System Running"}
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import report_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_controller.router)

@app.get("/")
def home():
    return {"message": "Report System Running"}