import sshtunnel
from sqlalchemy import create_engine
from sqlalchemy import text


tunnel = sshtunnel.SSHTunnelForwarder(
    ("ssh.pythonanywhere.com"),
    ssh_username="Polonez",
    ssh_password="Lacosanostra1#",
    remote_bind_address=("Polonez.mysql.pythonanywhere-services.com", 3306),
)
tunnel.start()

engine = create_engine(
    f"mysql+mysqldb://Polonez:lacosanostra@127.0.0.1:{tunnel.local_bind_port}/Polonez$default"
)
connection = engine.connect()
result = connection.execute(text("SELECT 1"))
for row in result:
    print(row)
engine.dispose()

tunnel.close()
