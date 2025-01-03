from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI()


class Reserva(BaseModel):
    nombre: str
    apellidos: str
    vehiculo: str
    modelo: str
    fecha_ingreso: date = Field(..., description="Fecha de ingreso en formato YYYY-MM-DD")
    fecha_salida: date = Field(..., description="Fecha de salida en formato YYYY-MM-DD")
    

@app.post("/api/reservas/")
async def create_reserva(reserva: Reserva):
    try:
        guardar_en_base_datos(reserva)
        return {"mensaje": "Reserva creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al guardar la reserva")
    
def guardar_en_base_datos(reserva):
    print("Datos guardados en base de datos simulada:")
    print(reserva.dict())
