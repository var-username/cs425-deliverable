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

    def commit(self):
        self._conn.commit()

    def connect(self, **kwargs):
        for key in kwargs.keys():
            self._conf[key] = kwargs[key]
        self._conn = psycopg2.connect(**self._conf)
        self._cur = self._conn.cursor()

    def create_index(self, index: str, schema: str, table: str, *params):
        # TODO
        # CREATE INDEX IF NOT EXISTS {indexname} ON {schema}.{table} {params}
        raise NotImplementedError

    def create_role(self, name: str, perms: list[str]):
        # TODO
        # CREATE ROLE {name} WITH {permissions};
        command = "CREATE ROLE {0}"
        if len(perms) > 0:
            command += " WITH "
            command += " ".join(perms)
        query = sql.SQL(command).format(sql.Identifier(name))
        self.execute(query)

    def create_schema(self, schema: str, group: str):
        command = "CREATE SCHEMA IF NOT EXISTS {0} "
        if group is not None:
            command += "AUTHORIZATION {1}"
        self.execute(command.format(schema, group))

    def create_table(self, schema: str, table: str, *columns: list[(str, str, str)], constraints: list[(str, str)]):
        # TODO
        # CREATE TABLE IF NOT EXISTS {schema}.{table}
        #
        # for column in columns:
        #   ADD COLUMN IF NOT EXISTS {colname} {datatype} {constraint}
        #
        # for constraint in constraints:
        #   ADD CONSTRAINT {constraintname} {constraintargs}
        raise NotImplementedError

    def create_user(self, user: str, role: str, *args):
        command = str('''CREATE USER {user}''')

        if role is not None:
            command += ''' IN GROUP {role} '''

        command += ''' '''.join(args)

        self.execute(sql.SQL(command).format(
            user=sql.Literal(user), role=sql.Literal(role)))

    def does_role_exist(self, role: str) -> bool:
        try:
            self.list_roles().index(role)
            return True
        except ValueError as e:
            return False

    def does_schema_exist(self, schema: str) -> bool:
        try:
            self.list_schemas().index(schema)
            return True
        except ValueError as e:
            return False

    def execute(self, query):
        if self._cur is None:
            raise Exception()
        else:
            return self._cur.execute(query)

    def forget_all(self):
        self._conf = dict()

    def list_roles(self) -> list[str]:
        self.execute(sql.SQL("SELECT rolname FROM {}").format(sql.Identifier("pg_catalog", "pg_roles")))
        results = list()
        for item in self._cur.fetchall():
            results.append(item[0])
        return results

    def list_schemas(self) -> list[str]:
        self.execute(sql.SQL("SELECT nspname FROM {}").format(sql.Identifier("pg_catalog", "pg_namespace")))
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

    def rollback(self):
        self._conn.rollback()

    def set_user_password(self, user: str, password: str):
        if password is None or password == "":
            password = "NULL"
        self.execute(sql.SQL("ALTER ROLE {role} WITH PASSWORD {password}").format(
            role=sql.Literal(user), password=sql.Literal(password)))
