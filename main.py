from fastapi import FastAPI

from src.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {
        "message": "Contact Management API is up and running!",
        "next_steps": "Please visit the /docs endpoint for detailed API "
        "documentation and interactive exploration of endpoints."
    }