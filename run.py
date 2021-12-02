#!/bin/env/python3

import argparse
import os
import getpass

from src import connection

if __name__ == '__main__':

    conf = dict()

    # === Arguments ===

    argparser = argparse.ArgumentParser(description='CS425')

    #argparser.add_argument('-n', '--no-ncurses', action="store_false", help='disables the ncurses tui')
    argparser.add_argument('-v', '--verbose', action="store_true",
                           help='runs the program in verbose mode')
    argparser.add_argument('-H', '--host', action="store",
                           help='the host to connect to')
    argparser.add_argument('-p', '--port', action="store",
                           help='the port to connect to')
    argparser.add_argument('-d', '--dbname', action="store",
                           help='the database name')
    argparser.add_argument('-u', '--user', action="store",
                           help='the username to connect to the database with')
    argparser.add_argument('-P', '--password', action="store",
                           help='the password to authenticate with')
    argparser.add_argument('-S', '--schema', action="store")

    args = argparser.parse_args()

    for arg in ['host', 'port', 'dbname', 'user', 'password', 'schema']:
        if args.__dict__[arg] is not None:
            conf[arg] = str(args.__dict__[arg]).lstrip()
            if conf[arg] == '.':
                conf[arg] = ''
        else:
            conf[arg] = None

    if args.verbose:
        print("Verbose mode on.")

    # Get Creds and stuff

    if conf['host'] is None:
        print("Please input the database host (defaults to UNIX socket if empty)")
        conf['host'] = input('> ')
    elif args.verbose:
        print("Host already passed as {0}".format(args.host))

    if conf['port'] is None:
        print("Please input the database port (defaults to 5432 if empty)")
        conf['port'] = input('> ')
        if conf['port'].strip() == "":
            conf['port'] = 5432
    elif args.verbose:
        print("Port already passed as {0}".format(args.port))

    if conf['dbname'] is None:
        print("Please input the database name (defaults to \'Database1\' if empty)")
        conf['dbname'] = input('> ')
        if conf['dbname'].strip() == "":
            conf['dbname'] = 'Database1'
    elif args.verbose:
        print("dbname already passed as {0}".format(args.dbname))

    if conf['user'] is None:
        print("Please input the username to authenticate with (defaults to your OS username if empty)")
        conf['user'] = input('> ')
        if conf['user'].strip() == "":
            conf['user'] = getpass.getuser()
    elif args.verbose:
        print("User already passed as {0}".format(args.user))

    if conf['password'] is None:
        print(
            "Please input the password to authenticate with (your input will not be echoed)")
        conf['password'] = getpass.getpass('$ ')
    elif args.verbose:
        print("Password already passed as {0}".format(args.password))

    if args.verbose:
        print("conf: ", conf)

    # Make connection from creds

    conn = connection.Connection(**conf)
    if args.verbose:
        print("Connection object created")

    # Establish connection to db

    conn.connect()
    if args.verbose:
        print("Connection established")

    # Check if admin, doctor, and patient exist
    # Create them if they don't

    admin_existed = True
    doctor_existed = True
    patient_existed = True

    if not conn.does_role_exist('admin'):
        conn.create_role('admin', ['CREATEROLE'])
        admin_existed = False

    if not conn.does_role_exist('doctor'):
        conn.create_role('doctor', [])
        doctor_existed = False

    if not conn.does_role_exist('patient'):
        conn.create_role('patient', [])
        patient_existed = False

    # Select schema
    
    if conf['schema'] is None:
        print("\nPlease select your schema.\n\nAvailable schemas:")
        print("(If an approprate schema does not exist input \'N/A\')")
        print(conn.list_schemas())
        conf['schema'] = input('> ').strip()
    elif args.verbose:
        print("Schema already passed as {0}".format(args.schema))

    new_schema = False

    if conf['schema'] == 'N/A':
        # If schema input is 'N/A', create a new schema
        print("What should the schema be called?")
        conf['schema'] = input('> ').strip()
        new_schema = True
        conn.create_schema(conf['schema'], "admin")
        conn.commit()
    else:
        if conn.does_schema_exist(conf['schema']):
            print("\nAvailable tables:")
            print(conn.list_tables_in_schema(conf['schema']))
        else:
            print("Schema does not exist!")
            exit(1)

    if new_schema:
        # TODO: Create Tables and stuff
        # NOTE: Maybe we can do batch CREATE queries here, and do the
        #       ALTER queries in the else block?
        pass
    else:
        pass
