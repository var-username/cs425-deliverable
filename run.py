#!/bin/env/python3

import argparse
import getpass
import psycopg2.sql as sql

from src import connection, menu

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
        print("V) Verbose mode on.")

    # Get Creds and stuff

    if conf['host'] is None:
        print("Please input the database host (defaults to UNIX socket if empty)")
        conf['host'] = input('> ')
    elif args.verbose:
        print("V) Host already passed as{0}".format(args.host))

    if conf['port'] is None:
        print("Please input the database port (defaults to 5432 if empty)")
        conf['port'] = input('> ')
        if conf['port'].strip() == "":
            conf['port'] = 5432
    elif args.verbose:
        print("V) Port already passed as{0}".format(args.port))

    if conf['dbname'] is None:
        print("Please input the database name (defaults to \'Database1\' if empty)")
        conf['dbname'] = input('> ')
        if conf['dbname'].strip() == "":
            conf['dbname'] = 'Database1'
    elif args.verbose:
        print("V) dbname already passed as{0}".format(args.dbname))

    if conf['user'] is None:
        print("Please input the username to authenticate with (defaults to your OS username if empty)")
        conf['user'] = input('> ')
        if conf['user'].strip() == "":
            conf['user'] = getpass.getuser()
    elif args.verbose:
        print("V) User already passed as{0}".format(args.user))

    if conf['password'] is None:
        print(
            "Please input the password to authenticate with (your input will not be echoed)")
        conf['password'] = getpass.getpass('$ ')
    elif args.verbose:
        print("V) Password already passed as{0}".format(args.password))

    if args.verbose:
        print("V) conf: ", conf)

    # Make connection from creds

    conn = connection.Connection(**conf)
    if args.verbose:
        print("V) Connection object created")

    # Establish connection to db

    conn.connect()
    if args.verbose:
        print("V) Connection established")

    # Set user if it's empty

    if conf['user'] == '':
        conn.execute(sql.SQL("SELECT current_user;"))
        conf['user'] = conn._cur.fetchone()[0]
        if args.verbose:
            print("V) Current user is " + conf['user'])

    # Check if admin, doctor, and patient exist
    # Create them if they don't

    admin_existed = True
    doctor_existed = True
    patient_existed = True

    if not conn.does_role_exist('admin'):
        print("V) Role 'admin' does not exist")
        conn.create_role('admin', ['CREATEROLE'])
        print("V) Admin role created")
        admin_existed = False

    if not conn.does_role_exist('doctor'):
        print("V) Role 'doctor' does not exist")
        conn.create_role('doctor', [])
        print("V) Doctor role created")
        doctor_existed = False

    if not conn.does_role_exist('patient'):
        print("V) Role 'patient' does not exist")
        conn.create_role('patient', [])
        print("V) Patient role created")
        patient_existed = False

    # Select schema

    if conf['schema'] is None:
        print("\nPlease select your schema.\n\nAvailable schemas:")
        print("(If an approprate schema does not exist input 'N/A')")
        print(conn.list_schemas())
        conf['schema'] = input('> ').strip().lower()
    elif args.verbose:
        print("V) Schema already passed as{0}".format(args.schema))

    # If the schema does not exist, prompt for name

    new_schema = False

    if conf['schema'] == 'N/A':
        # If schema input is 'N/A', create a new schema
        print("What should the schema be called?")
        conf['schema'] = input('> ').strip().lower()
        new_schema = True
        print("V) Creating schema " + conf['schema'])
        conn.create_schema(conf['schema'], "admin")
        print("V) Schema '" + conf['schema'] + "' created")
        conn.commit()
    else:
        if not conn.does_schema_exist(conf['schema']):
            print("Schema does not exist!")
            exit(1)

    # If the schema is new, generate structure from SCHEMA.sql in cwd

    if new_schema:
        f = open("SCHEMA.sql")
        if args.verbose:
            print("V) Creating database from SCHEMA.sql")
        conn.execute(sql.SQL(f.read()).format(
            schema=sql.Identifier(conf['schema'].strip().lower())))
        if args.verbose:
            print("V) Database created")
        conn.commit()
    
    # Welcome prompt

    print("Welcome " + conf['user'] + ", your current role is " + conn.get_user_highest_role(conf["user"]))
    print("\nWhat would you like to do? (Entering ? will show the help page)")

    # Keep showing menu until program close

    loop = True

    while(loop):
        loop = menu.main_menu(conf, conn)

    conn.commit()
