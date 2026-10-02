import pandas as pd
import sqlite3
import os

def limpiar_monto(valor):
    if pd.isna(valor):
        return None
    # Convertir a string y quitar símbolos de moneda y espacios
    valor = str(valor).replace('$', '').replace(' ', '').strip()
    
    # Regla: Si tiene punto y coma (12,500.50), la coma es separador de miles
    if ',' in valor and '.' in valor:
        valor = valor.replace(',', '')
    # Regla: Si tiene solo coma (12500,50), la coma es el separador decimal
    elif ',' in valor and '.' not in valor:
        valor = valor.replace(',', '.')
        
    try:
        monto_float = float(valor)
        # Regla: Descartar montos negativos
        if monto_float < 0:
            return None
        return monto_float
    except ValueError:
        return None

def procesar_ventas():
    print("Iniciando lectura y limpieza de datos...")
    
    # 1. Leer archivo asegurando la codificación UTF-8 sin BOM
    ruta_csv = os.path.join('data', 'ventas.csv')
    # Subimos un nivel en la ruta relativa si ejecutamos desde dentro de src, 
    # pero como ejecutaremos desde la raíz, usamos 'data/ventas.csv' directamente.
    ruta_csv = '../data/ventas.csv' if os.path.basename(os.getcwd()) == 'src' else 'data/ventas.csv'
    
    df = pd.read_csv(ruta_csv, encoding='utf-8')
    
    # 2. Limpieza y validación de Región
    df = df.dropna(subset=['region']) # Descartar fila si región está vacía
    df['region'] = df['region'].astype(str).str.lower().str.strip()
    
    # 3. Limpieza y homologación de Estatus
    df['estatus'] = df['estatus'].astype(str).str.lower().str.strip()
    reemplazos_estatus = {
        'cerrado': 'cerrada',
        'abierto': 'abierta',
        'cancelado': 'cancelada'
    }
    df['estatus'] = df['estatus'].replace(reemplazos_estatus)
    
    # 4. Limpieza de Montos
    df['monto'] = df['monto'].apply(limpiar_monto)
    df = df.dropna(subset=['monto']) # Descartar inválidos
    
    # 5. Normalizar y validar Fechas
    # dayfirst=True asegura que '04-03-2026' sea el 4 de marzo
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['fecha']) # Descartar fechas inválidas (NaT)
    # Convertir a formato de base de datos YYYY-MM-DD
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    
    # 6. Deduplicar por id_venta
    df = df.drop_duplicates(subset=['id_venta'], keep='first')
    
    # 7. Almacenar en base de datos SQLite
    ruta_db = '../ventas.db' if os.path.basename(os.getcwd()) == 'src' else 'ventas.db'
    conn = sqlite3.connect(ruta_db)
    
    # Guardamos en la tabla 'ventas'
    df.to_sql('ventas', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Proceso completado exitosamente. Se guardaron {len(df)} registros válidos en ventas.db.")

if __name__ == "__main__":
    procesar_ventas()