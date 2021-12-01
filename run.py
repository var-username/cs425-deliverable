#!/bin/env/python3

import argparse
import os
import getpass

from src import connection

if __name__ == '__main__':

    # === Arguments ===
    argparser = argparse.ArgumentParser(description='CS425')

    #argparser.add_argument('-n', '--ncurses', action="store_true", help='enables the ncurses tui')
    argparser.add_argument('-v', '--verbose', action="store_true",
                           help='runs the program in verbose mode')

    args = argparser.parse_args()

    if args.verbose:
        print("Verbose mode on.")

    # Get Creds and stuff
    conf = dict()
    print("Please input the database host (defaults to UNIX socket if empty)")
    conf['host'] = input('> ')

    print("Please input the database port (defaults to 5432 if empty)")
    conf['port'] = input('> ')
    if conf['port'].strip() == "":
        conf['port'] = 5432

    print("Please input the database name (defaults to \'Database1\' if empty)")
    conf['dbname'] = input('> ')
    if conf['dbname'].strip() == "":
        conf['dbname'] = 'Database1'

    print("Please input the username to authenticate with (defaults to your OS username if empty)")
    conf['user'] = input('> ')
    if conf['user'].strip() == "":
        conf['user'] = getpass.getuser()

    print("Please input the password to authenticate with (your input will not be echoed)")
    conf['password'] = getpass.getpass('$ ')

    if args.verbose:
        print("conf: ", conf)

    conn = connection.Connection(**conf)
    if args.verbose:
        print("Connection object created")

    # Establish connection to db
    conn.connect()
    if args.verbose:
        print("Connection established")

    # Select schema
    print("\nPlease select your schema.\n\nAvailable schemas:")
    print(conn.list_schemas())

    schema = input('> ').strip()

    print("\nAvailable tables:")
    print(conn.list_tables_in_schema(schema))

    # Create schema if not existant
