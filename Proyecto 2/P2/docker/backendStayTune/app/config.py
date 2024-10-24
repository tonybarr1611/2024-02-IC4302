#Config of the environment variables for the connections to the databases 
import os

POSTGRES_USER = os.getenv('POSTGRES_USER', 'tu_usuario')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'tu_contraseña')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

print(f"POSTGRES_USER: {POSTGRES_USER}")