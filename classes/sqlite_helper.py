import sqlite3

class DatabaseLite:
    def __init__(self, database_filename):
        self.database_filename = database_filename
        self._db = sqlite3.connect(database_filename)

    def run_query(self, sql):
        cursor = self._db.execute(sql)
        rows = cursor.fetchall()
        # return dict(cursor.fetchone())
        return rows

    # def sql_do(self, sql, *params):
    #     self._db.execute(sql, params)
    #     self._db.commit()

    # def insert(self, row):
    #     self._db.execute('insert into {} (t1, i1) values (?, ?)'.format(self._table), (row['t1'], row['i1']))
    #     self._db.commit()

    # def retrieve(self, key):
    #     cursor = self._db.execute('select * from {} where t1 = ?'.format(self._table), (key,))
    #     return dict(cursor.fetchone())

    # def update(self, row):
    #     self._db.execute(
    #         'update {} set i1 = ? where t1 = ?'.format(self._table),
    #         (row['i1'], row['t1']))
    #     self._db.commit()

    # def delete(self, key):
    #     self._db.execute('delete from {} where t1 = ?'.format(self._table), (key,))
    #     self._db.commit()

    # def disp_rows(self):
    #     cursor = self._db.execute('select * from {} order by t1'.format(self._table))
    #     for row in cursor:
    #         print('  {}: {}'.format(row['t1'], row['i1']))

    # def __iter__(self):
    #     cursor = self._db.execute('select * from {} order by t1'.format(self._table))
    #     for row in cursor:
    #         yield dict(row)

    # @property
    # def filename(self): return self._filename
    # @filename.setter
    # def filename(self, fn):
    #     self._filename = fn
    #     self._db = sqlite3.connect(fn)
    #     self._db.row_factory = sqlite3.Row
    # @filename.deleter
    # def filename(self): self.close()
    # @property
    # def table(self): return self._table
    # @table.setter
    # def table(self, t): self._table = t
    # @table.deleter
    # def table(self): self._table = 'test'

    # def close(self):
    #         self._db.close()
    #         del self._filename