import psycopg2.sql as sql

from src import connection


def main_menu(conf: dict, conn: connection.Connection) -> bool:
    role = conn.get_user_highest_role(conf["user"])

    try:
        command = input('> ').strip().split(' ')
    except KeyboardInterrupt:
        exit(0)

    if command[0].startswith('?'):
        print_help(role)

    elif command[0].startswith('q'):
        return False

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

    elif command[0].startswith('c'):

        if (command[1].startswith('?') or len(command) < 2):
            print("Usage: c [item] ...")

        elif command[1].startswith('u'):
            if (command[2].startswith('?') or len(command) < 4):
                print("Usage: c u [username] [group] (args)")
            else:
                conn.create_user(*command[2:])
                conn.commit()

    elif command[0].startswith('C'):
        conn.commit()

    elif command[0].startswith('R'):
        conn.rollback()

    return True


def print_help(role: str):
    if(role == 'admin'):
        # Admin actions
        print("(c)reate new")
        print("  (u)ser")
        print("")
        pass
    elif (role == 'doctor' or role == 'admin'):
        # Doctor actions
        print("(a)dd new")
        print("  (d)onor")
        print("  (o)rgan")
        print("  (p)atient")
        print("")
        pass
    elif(role == 'patient' or role == 'doctor' or role == 'admin'):
        # Patient actions
        print("(C)ommit (debug command)")
        print("(R)evert (debug command)")
        print("")
        pass
    else:
        # Role is unknown
        pass

    print("(q)uit")
