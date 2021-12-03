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
                    if (command[1].startswith('?') or len(command) < 4):
                        print(
                            '''Usage: a d [donorid] [donorname] (organname) (bloodtype) (region) (age)\n\t
                            (lastdonation) (phone) (email) (chronicaldisease) (druguse) (lasttattoo) (medicalhistory)
                            ''')
                    else:
                        query = sql.SQL("insert into {table} ({}) values ({})").format(
                            sql.SQL(", ").join(map(sql.Identifier, [
                                'donorid', 'donorname', 'organname', 'bloodtype', 'region', 'age', 'lastdonation', 'phone', 'email', 'chronicaldisease', 'druguse', 'lasttattoo', 'medicalhistory'][:len(command)-2])),
                            sql.SQL(", ").join(
                                sql.Placeholder() * (len(command) - 2)),
                            table=sql.Identifier(conf['schema'], "organ"))
                        conn.execute(query, command[2:])

                elif (command[1].startswith('o')):
                    # Add new organ
                    if (command[1].startswith('?') or len(command) < 6):
                        print(
                            "Usage: a o [doctorid] [organid] [donorid] [hospitalid] (organname) (life_hrs) (availibilitydate)")
                    else:
                        query = sql.SQL("insert into {table} ({}) values ({})").format(
                            sql.SQL(", ").join(map(sql.Identifier, [
                                'doctorid', 'organid', 'donorid', 'hospitalid', 'organname', 'life_hrs', 'availibiliydate'][:len(command)-2])),
                            sql.SQL(", ").join(
                                sql.Placeholder() * (len(command) - 2)),
                            table=sql.Identifier(conf['schema'], "organ"))
                        conn.execute(query, command[2:])

                elif (command[1].startswith('p')):
                    # Add new patient
                    if (command[1].startswith('?') or len(command) < 4):
                        print(
                            "Usage: a p [id] [bloodtype] (name) (region) (age) (drug history) (allergies)")
                    else:
                        query = sql.SQL("insert into {table} ({}) values ({})").format(
                            sql.SQL(", ").join(map(sql.Identifier, [
                                'patientid', 'bloodtype', 'patientname', 'region', 'age', 'drughistory', 'allergies'][:len(command)-2])),
                            sql.SQL(", ").join(
                                sql.Placeholder() * (len(command) - 2)),
                            table=sql.Identifier(conf['schema'], "patient"))
                        conn.execute(query, command[2:])

            # Income report
            # > I
            elif command[0].startswith('i'):
                query = sql.SQL(
                    '''
                    SELECT hospitalid, hospitalName, region, sum(hospitalizationcost)
                    FROM {table1} natural join {table2}
                    group by hospitalid;
                    ''').format(table1=sql.Identifier(conf['schema'], 'Hospital'), table2=sql.Identifier(conf['schema'], 'treated'))
                conn.execute(query)
                print('Hospitals: (id, name, region, income)')
                for record in conn._cur:
                    print(record)

            # Organ match list
            elif command[0].startswith('m'):
                query = sql.SQL('''
                    with patientneeds as (select patientid, region, bloodtype, patient_needs.need
                        from {patientt} natural join {patientneedst})
                    SELECT D.donorid, patientid, o.availibilitydate, o.organname, o.organid FROM 
                        {donort} D, patientneeds P, {organt} O WHERE
                    D.organname = P.need and D.region = P.region
                    AND (P.bloodtype = 'AB' OR D.bloodtype = 'O' OR P.bloodtype = D.bloodtype)
                    AND O.life_hrs > 0;
                ''').format(
                    patientt=sql.Identifier(conf['schema'], 'patient'),
                    patientneedst=sql.Identifier(
                        conf['schema'], 'patient_needs'),
                    donort=sql.Identifier(conf['schema'], 'donor'),
                    organt=sql.Identifier(conf['schema'], 'organ')
                )
                conn.execute(query)
                print(
                    "All matching donations: (donorid, patientid, availdate, organ, organid)")
                for record in conn._cur:
                    print(record)

            # Search
            # > s
            elif command[0].startswith('s'):

                if (command[1].startswith('?') or len(command) < 4):
                    print("Usage: s [b, o] [type] [region]")

                elif command[1].startswith('b'):
                    if (command[2].startswith('?') or len(command) < 4):
                        print("Usage: s b [bloodtype] [region]")
                    else:
                        targetdate = datetime.date.today() - datetime.timedelta(days=30)
                        query = sql.SQL("SELECT donorid, donorname FROM {table} WHERE bloodtype = {bloodtype} and organname = 'blood' and lastdonation >= {curdate} and region = {region}").format(
                            table=sql.Identifier(conf['schema'], 'donor'), bloodtype=sql.Literal(command[2]), region=sql.Literal(command[3]), curdate=sql.Literal(targetdate.isoformat()))
                        conn.execute(query)
                        print("Patients: (id, name)")
                        for record in conn._cur:
                            print(record)

                elif command[1].startswith('o'):
                    if (command[1].startswith('?') or len(command) < 4):
                        print("Usage: s o [organname] [region]")
                    else:
                        query = sql.SQL('''
                            with tempTable as (select donorid, donor.region, organname, doctorname 
                            from {donort} inner join {doctort} on organname = doctor.specialization
                            where {donort}.region = {doctort}.region)
                            select donorid, organname, doctorname from tempTable
                            where organname = {organ} and region = {region}
                        ''').format(donort=sql.Identifier(conf['schema'], 'donor'), doctort=sql.Identifier(conf['schema'], 'doctor'),
                                    organname=sql.Literal(command[2]), region=sql.Literal(command[3]))
                        conn.execute(query)
                        print("Donors: (id, region, organ, local doctor)")
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
        print("(i)ncome report")
        print("organ (m)atch list")
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
