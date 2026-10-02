from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import sqlite3
from datetime import datetime
import os

app = FastAPI(title="Nuwek KPI API")

def get_db_connection():
    # Asegurar la ruta correcta a la base de datos
    ruta_db = '../ventas.db' if os.path.basename(os.getcwd()) == 'src' else 'ventas.db'
    conn = sqlite3.connect(ruta_db)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/ventas/resumen")
def resumen_ventas(
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD")
):
    # 1. Validar parámetros de fecha
    if fecha_inicio or fecha_fin:
        if not (fecha_inicio and fecha_fin):
            raise HTTPException(status_code=400, detail="Debes proporcionar ambas fechas o ninguna.")
        
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            if inicio > fin:
                raise HTTPException(status_code=400, detail="fecha_inicio no puede ser posterior a fecha_fin")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Debe ser YYYY-MM-DD")

    # 2. Conectar a la BD y preparar la consulta
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Solo consideramos estatus 'cerrada'
    query_base = "FROM ventas WHERE estatus = 'cerrada'"
    params = []

    if fecha_inicio and fecha_fin:
        query_base += " AND fecha >= ? AND fecha <= ?"
        params.extend([fecha_inicio, fecha_fin])
    
    # 3. Calcular Totales
    cursor.execute(f"SELECT SUM(monto) as total, COUNT(*) as cantidad {query_base}", params)
    totales = cursor.fetchone()
    
    total_ventas = round(totales['total'], 2) if totales['total'] is not None else 0.0
    numero_ventas = totales['cantidad']

    # 4. Calcular por Región
    cursor.execute(f"""
        SELECT region, SUM(monto) as total_region 
        {query_base} 
        GROUP BY region 
        ORDER BY total_region DESC
    """, params)
    
    por_region = [{"region": row["region"].capitalize(), "total": round(row["total_region"], 2)} for row in cursor.fetchall()]
    conn.close()

    # 5. Retornar JSON en el formato exacto solicitado
    return {
        "total_ventas": total_ventas,
        "numero_ventas": numero_ventas,
        "por_region": por_region
    }