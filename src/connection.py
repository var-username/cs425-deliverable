import psycopg2
import psycopg2.sql as sql


class Connection(object):

    def __init__(self, **kwargs):
        self._conf = dict()
        for key in kwargs.keys():
            self._conf[key] = kwargs[key]

    def close(self):
        if self._conn is not None:
            self._conn.close()

    def connect(self, **kwargs):
        for key in kwargs.keys():
            self._conf[key] = kwargs[key]
        self._conn = psycopg2.connect(**self._conf)
        self._cur = self._conn.cursor()

    def create_schema(self, schema: str):
        raise NotImplementedError

    def create_table(self, schema: str, table: str):
        raise NotImplementedError

    def create_user(self, user: str, role: str, *args):
        command = str('''CREATE USER {user}''')

        if role is not None:
            command += ''' IN GROUP {role} '''

        command += ''' '''.join(args)

        self.execute(sql.SQL(command).format(
            user=sql.Literal(user), role=sql.Literal(role)))

    def does_schema_exist(self, schema: str) -> bool:
        try:
            self.list_schemas().index(schema)
            return True
        except ValueError as e:
            return False

    def does_table_match(self, schema: str, table: str):
        raise NotImplementedError

    def execute(self, query):
        if self._cur is None:
            raise Exception()
        else:
            return self._cur.execute(query)

    def forget_all(self):
        self._conf = dict()

    def list_schemas(self) -> list[str]:
        self.execute(sql.SQL("SELECT nspname FROM pg_catalog.pg_namespace"))
        results = list()
        for item in self._cur.fetchall():
            results.append(item[0])
        return results

    def list_tables_in_schema(self, schema: str) -> list[str]:
        self.execute(
            sql.SQL("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = {schema}").
            format(schema=sql.Literal(schema)))
        results = list()
        for item in self._cur.fetchall():
            results.append(item[0])
        return results

    def set_user_password(self, user: str, password: str):
        if password is None or password == "":
            password = "NULL"
        self.execute(sql.SQL("ALTER ROLE {role} WITH PASSWORD {password}").format(
            role=sql.Literal(user), password=sql.Literal(password)))
