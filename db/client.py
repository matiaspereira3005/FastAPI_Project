import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Cargar variables desde .env (si existe)
load_dotenv()

# Leer únicamente desde variables de entorno (sin valores por defecto)
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")
ATLAS_URI = os.getenv("ATLAS_URI")


# Priorizar conexión Atlas si se proporciona en .env
if ATLAS_URI:
	# Conexión a MongoDB Atlas (cluster).
	# Nota: tlsInsecure=True desactiva la verificación del certificado (solo para desarrollo)
	db_client = MongoClient(ATLAS_URI, server_api=ServerApi("1"), tlsInsecure=True).test
else:
	# Conexión local (comentada) — mantener para referencia, pero sin valores en duro
	# MONGO_USER = MONGO_USER or "admin"
	# MONGO_PASSWORD = MONGO_PASSWORD or "admin123"
	# MONGO_HOST = MONGO_HOST or "localhost"
	# MONGO_PORT = MONGO_PORT or "27017"
	# MONGO_AUTH_DB = MONGO_AUTH_DB or "admin"
	# MONGO_URI = (
	#     f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource={MONGO_AUTH_DB}"
	# )
	# db_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000).test
	db_client = None
