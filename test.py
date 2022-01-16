import sqlite3
import os
from classes.sqlite_helper import DatabaseLite


if __name__ == "__main__":
    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)
    sql = "select * from goods_nomenclatures limit 10;"
    rows = db.run_query(sql)
    for row in rows:
        print(row[0])
    print("Done")
