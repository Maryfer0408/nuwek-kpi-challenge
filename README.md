# Nuwek KPI Challenge - API de Resumen de Ventas

Solución al reto técnico para la vacante de Practicante de Desarrollo y Datos en Grupo Nuwek. El proyecto consiste en un pipeline de datos (ETL) ligero y una API RESTful para consultar los indicadores comerciales.

## 1. Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Análisis y Limpieza de Datos:** Pandas
* **Base de Datos:** SQLite3 (ligera, ideal para pruebas y sin configuración de servidor)
* **Framework Web API:** FastAPI (con Uvicorn)
* **Control de Versiones:** Git / GitHub

## 2. Cómo instalar el proyecto
1. Clona este repositorio:
   ```bash
   git clone https://github.com/Maryfer0408/nuwek-kpi-challenge.git
   cd nuwek-kpi-challenge

1.Crea y activa un entorno virtual:
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

2.Instala las dependencias necesarias:
pip install -r requirements.txt

3. Cómo configurar la base de datos
La base de datos SQLite (ventas.db) se genera automáticamente al ejecutar el script de procesamiento de datos. No se requiere instalación de un gestor de base de datos externo.

4. Cómo importar/procesar ventas.csv
El archivo original debe estar ubicado en data/ventas.csv. Para ejecutar la limpieza y poblar la base de datos, ejecuta en la terminal desde la raíz del proyecto:
python src/etl.py
Esto aplicará las reglas de negocio, normalizará los formatos y creará la tabla ventas en ventas.db.

5. Cómo ejecutar la aplicación
Levanta el servidor local con FastAPI utilizando Uvicorn:
uvicorn src.main:app --reload
La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

6. Cómo probar el endpoint
Puedes probar la API desde la documentación interactiva generada por Swagger ingresando a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), o utilizar un comando curl:

Resumen histórico (todas las fechas):
curl -X GET "http://127.0.0.1:8000/api/ventas/resumen"

Resumen filtrado por fechas:
curl -X GET "http://127.0.0.1:8000/api/ventas/resumen?fecha_inicio=2026-01-01&fecha_fin=2026-03-31"

7. Problemas encontrados en los datos y decisiones tomadas
Durante el análisis de ventas.csv se encontraron inconsistencias intencionales que se resolvieron mediante Pandas en etl.py:

Montos económicos: Contenían espacios vacíos, símbolos $ y variaciones en los separadores decimales y de miles. Se implementó una lógica de limpieza utilizando replace para identificar que, si el valor contenía coma y punto, la coma era separador de miles; si solo contenía coma, fungía como decimal. Los valores negativos y no numéricos fueron descartados.

Fechas inconsistentes: Se detectó la mezcla de formatos YYYY-MM-DD y DD-MM-YYYY. Se utilizó pd.to_datetime con el parámetro dayfirst=True para garantizar que días y meses no se invirtieran (ej. el día 4 se leyó como marzo, no abril). Los valores NaT (vacíos o imposibles) fueron descartados.

Texto no estandarizado: Las columnas region y estatus presentaban mayúsculas intercaladas y espacios sobrantes. Se normalizaron usando .str.lower().str.strip().

Duplicados: Se utilizó drop_duplicates basado en la llave primaria id_venta manteniendo la primera coincidencia limpia.

8. Manejo de una API Key
Las API Keys y credenciales sensibles nunca deben almacenarse en el código fuente ni subirse al control de versiones.
Para el entorno de desarrollo, almacenaría la API Key en un archivo local .env (el cual debe estar ignorado en el .gitignore). En un entorno de producción, utilizaría un Gestor de Secretos (como AWS Secrets Manager, GitHub Secrets o HashiCorp Vault) e inyectaría la credencial como una variable de entorno directamente en el servidor al momento del despliegue.

9. Integración con un SaaS
Para conectar nuestra API con un SaaS operativo sin intervenir ni poner en riesgo su base de datos actual, desarrollaría un servicio intermediario o worker ligero (ej. un Cron Job o script programado). Este servicio tendría la única responsabilidad de consumir nuestro endpoint /api/ventas/resumen, mapear o transformar el JSON al payload exacto que requiera el SaaS, y enviarlo mediante peticiones seguras (HTTP POST) a la API pública del SaaS. Esto mantiene a ambos sistemas totalmente desacoplados.

10. Herramientas de IA utilizadas
Se utilizó la IA como asistente de pair-programming para estructurar las buenas prácticas del repositorio, optimizar la lógica en la limpieza de datos con Pandas y validar la configuración de FastAPI.

**Nota:** Proyecto entregado para evaluación técnica.

