import datetime

import psycopg2.errors as p2err
import psycopg2.sql as sql

from src import connection


def main_menu(conf: dict, conn: connection.Connection) -> bool:
    if conn._conn.Error == p2err.InFailedSqlTransaction:
        conn.rollback()

    role = conn.get_user_highest_role(conf["user"])

    try:
        command = input('> ').strip().split(' ')
    except KeyboardInterrupt:
        exit(0)

    # Print main help message
    # > ?
    if command[0].startswith('?'):
        print_help(role)

    # Quit the program
    # > q
    elif command[0].startswith('q'):
        conn.commit()
        return False

    # Commit anything that hasn't been commited yet
    # In theory this shouldn't need to be used
    # > C
    elif command[0].startswith('C'):
        conn.commit()

    # Revert anything that hasn't been commited yet
    # In theory this shouldn't need to be used
    # > R
    elif command[0].startswith('R'):
        conn.rollback()

    else:
        # All the functions that could error because of permissions errors
        try:
            # Create something (admin)
            # > c [?, u [name group (args)] ]
            if command[0].startswith('c'):
                if (command[1].startswith('?') or len(command) < 2):
                    print("Usage: c [item] ...")

                elif command[1].startswith('u'):
                    if (command[2].startswith('?') or len(command) < 4):
                        print("Usage: c u [username] [group] (args)")
                    else:
                        conn.create_user(*command[2:])
                        conn.commit()

            # Add new item
            # > a [?, d, o, p]
            elif command[0].startswith('a'):

                if (command[1].startswith('?')):
                    print("Usage: a [item] ...")

                elif (command[1].startswith('d')):
                    # Add new donor
                    raise NotImplementedError

                elif (command[1].startswith('o')):
                    # Add new organ
                    raise NotImplementedError

                elif (command[1].startswith('p')):
                    # Add new patient
                    raise NotImplementedError

            # Income report
            # > I
            elif command[0].startswith('I'):
                raise NotImplementedError

            # Search
            # > s
            elif command[0].startswith('s'):
                searched = False
                if (command[1].startswith('?') or len(command) < 4):
                    print("Usage: s [b, o] [type] [region]")

                elif command[1].startswith('b'):
                    if (command[2].startswith('?') or len(command) < 4):
                        print("Usage: s b [bloodtype] [region]")
                    else:
                        targetdate = datetime.date.today() - datetime.timedelta(days = 30)
                        query = sql.SQL("SELECT donorid, donorname FROM {table} WHERE bloodtype = {bloodtype} and organname = 'blood' and lastdonation >= {curdate} and region = {region}").format(
                            table=sql.Identifier(conf['schema'], 'donor'), bloodtype=sql.Literal(command[2]), region=sql.Literal(command[3]), curdate=sql.Literal(targetdate.isoformat()))
                        conn.execute(query)
                        searched = True
                elif command[1].startswith('o'):
                    if (command[1].startswith('?') or len(command) < 4):
                        print("Usage: s o [organname] [region]")
                    else:
                        searched = True
                        pass

                if searched:
                    print("Patients: (id, name)")
                    for record in conn._cur:
                        print(record)

        # NOTE: pylance claims this isn't allowed but it seems to work when I run it
        except p2err.InsufficientPrivilege as e:
            print(e.pgerror)
            print("Your transaction has automatically been canceled back.")
            conn._conn.cancel()
            conn.rollback()

    return True


def print_help(role: str):
    if(role == 'admin'):
        # Admin actions
        print("(c)reate new")
        print("  (u)ser")
        print("")
        pass
    if (role == 'doctor' or role == 'admin'):
        # Doctor actions
        print("(a)dd new")
        print("  (d)onor")
        print("  (o)rgan")
        print("  (p)atient")
        print("(I)ncome report")
        print("")
        pass
    if(role == 'patient' or role == 'doctor' or role == 'admin'):
        # Patient actions
        print("(C)ommit (debug command)")
        print("(R)evert (debug command)")
        print("")
        pass
    else:
        # Role is unknown
        pass

    print("(q)uit")
