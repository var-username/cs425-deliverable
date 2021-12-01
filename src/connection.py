from typing import Dict, Union

import psycopg2


class Connection(object):

    def __init__(self, **kwargs):
        self._conf = dict()
        for key in kwargs.keys():
            self._conf[key] = kwargs[key]

    def connect(self, **kwargs):
        for key in kwargs.keys():
            self._conf[key] = kwargs[key]
        self._conn = psycopg2.connect(**self._conf)
        self._cur = self._conn.cursor()

    def close(self):
        if self._conn is not None:
            self._conn.close()

    def execute(self, query):
        if self._cur is None:
            raise Exception()
        else:
            return self._cur.execute(query)

    def forget_all(self):
        self._conf = dict()

    def list_schemas(self) -> list[str]:
        self.execute('''SELECT nspname FROM pg_catalog.pg_namespace;''')
        results = list()
        for item in self._cur.fetchall():
            results.append(item[0])
        return results

    def list_tables_in_schema(self, schema: str) -> list[str]:
        self.execute('''SELECT tablename FROM "pg_tables" WHERE schemaname = \'{0}\''''.format(schema))
        results = list()
        for item in self._cur.fetchall():
            results.append(item[0])
        return results