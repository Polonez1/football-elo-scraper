import sys
import pandas as pd

sys.path.append("./SQL-Data-Load/")

import pySQL


class EloDataLoad:
    def __init__(self):
        self.sql = pySQL.SQL(
            host="localhost",
            database="testDB",
            # user="user",
            # password="pass",
            connect_type="MsSQL",
        )

    def load_data(self, df, table_name, truncate: bool):
        self.sql.load_data_to_SQL(
            df=df, table=f"{table_name}", truncate=truncate, batch_size=10
        )

    def truncate_table(self, table):
        self.sql.read_query(f"truncate table {table}")


if "__main__" == __name__:
    sql = EloDataLoad()
    # commit
