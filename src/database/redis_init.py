import redis

# Conexión
r = redis.Redis(host='localhost', port=6379, db=0)

# Datos maestros (ID: Sueldo_Mensual)
master_data = {
    'CLI_001': 5000,
    'CLI_002': 2500,
    'CLI_003': 1200
}

def hydrate():
    for cli_id, salary in master_data.items():
        r.set(cli_id, salary)
    print("✅ Redis hidratado con sueldos de clientes.")

if __name__ == "__main__":
    hydrate()