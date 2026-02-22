import redis
import time

def hydrate_database():
    try:
        # Conexión al servicio de Redis definido en docker-compose
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        print("--- Iniciando Hidratación de Capa de Velocidad ---")
        
        # Datos maestros: ID de cliente y su sueldo mensual
        master_data = {
            'CLI_001': '5000',
            'CLI_002': '2800',
            'CLI_003': '1500',
            'CLI_004': '8000'
        }

        for cli_id, salary in master_data.items():
            r.set(cli_id, salary)
            print(f" Cargado: Cliente {cli_id} | Sueldo: S/ {salary}")

        print("--- Proceso completado con éxito ✅ ---")
        
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")

if __name__ == "__main__":
    hydrate_database()