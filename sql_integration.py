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

    def load_data(self, df, table_name):
        self.sql.load_data_to_SQL(
            df=df, table=f"{table_name}", truncate=False, batch_size=1000
        )

    def test():
        pass


if "__main__" == __name__:
    sql = EloDataLoad()
    # commit
