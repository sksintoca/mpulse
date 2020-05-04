import click, csv, os, sqlite3
# from mpulse.db import get_db

# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)


@click.command('readcsv')
@click.option('--name', prompt='csvfile', default="member_data_dups.csv",
              help='csvfile tom import.')
def readcsv(name):
    """Open db."""
    database = os.path.join(os.getcwd(), 'mpulse.db')
    schema = os.path.join(os.path.dirname(__file__), 'schema.sql')
    csvfile = os.path.join(os.path.dirname(__file__), name)
    click.echo(f'Import csv file: {csvfile}')

    conn = sqlite3.connect(database)
    click.echo('Connected to database.')

    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                columns = {", ".join(row)}
                click.echo(columns)
                line_count += 1
            else:
                columns = {"', '".join(row[1:])}
                fields = (row[1:])
                line_count += 1
                # # Insert a row of data
                insertsql = "INSERT INTO members (first_name, last_name, phone_number,client_member_id, account_id) VALUES (?, ?, ?, ?, ?)"
                try:
                    conn.execute(insertsql, fields )
                except sqlite3.IntegrityError:
                    click.echo(f'Line {line_count} was not unique {fields}')
                except:
                    click.echo(f'Line {line_count} failed insert {fields}')
                else:
                    click.echo(f'Line {line_count} sucess {fields}')
                finally:
                    pass
                # first_name TEXT UNIQUE NOT NULL,
                # last_name TEXT UNIQUE NOT NULL,
                # phone_number TEXT UNIQUE NOT NULL,
                # client_member_id TEXT NOT NULL UNIQUE,
                # account_id INTEGER NOT NULL
                # # Save (commit) the changes
                conn.commit()

        click.echo(f'lines {line_count}')
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        conn.close()


if __name__ == '__main__':
    readcsv(a)
