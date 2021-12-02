import psycopg2.sql as sql

from src import connection

def menu(conf: dict, conn: connection.Connection) -> bool:
    raise NotImplementedError