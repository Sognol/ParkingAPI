from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
import mysql.connector
from mysql.connector import Error

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
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parking"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()

            query = """INSERT INTO reservas (nombre, apellidos, vehiculo, modelo, fecha_ingreso, fecha_salida) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
            
            values = (
                reserva.nombre,
                reserva.apellidos,
                reserva.vehiculo,
                reserva.modelo,
                reserva.fecha_ingreso,
                reserva.fecha_salida
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            print("Reserva guardada correctamente en la base de datos.")
            
    except Error as e:
        print("Error al conectar con la base de datos:", {e})
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión con la base de datos cerrada.")