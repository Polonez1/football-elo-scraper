import sshtunnel
from sqlalchemy import create_engine
from sqlalchemy import text

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

tunnel = sshtunnel.SSHTunnelForwarder(
    ("ssh.pythonanywhere.com"),
    ssh_username="Polonez",
    ssh_password="Lacosanostra1#",
    remote_bind_address=("Polonez.mysql.pythonanywhere-services.com", 3306),
)
tunnel.start()

if tunnel.is_active:
    print("Tunnel is active and successfully established.")

print(1)
engine = create_engine(
    f"mysql+mysqlconnector://Polonez:lacosanostra@127.0.0.1:{tunnel.local_bind_port}/Polonez$default"
)
print(2)
connection = engine.connect()
print(3)
result = connection.execute(text("SELECT 1"))
for row in result:
    print(row)
engine.dispose()

tunnel.close()
