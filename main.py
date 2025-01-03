from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Home"])
async def home():
    return {"Saludo": "Inicio de la API de Parking"} 

