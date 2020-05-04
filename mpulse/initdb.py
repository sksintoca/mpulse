import os, click
import sqlite3
   

@click.command()
def initdb():
    """Clear the existing data and create new tables."""
    click.echo('Initialized the database.')
    database = os.path.join(os.getcwd(), 'mpulse.db')
    schema = os.path.join(os.path.dirname(__file__), 'schema.sql')

    conn = sqlite3.connect(database)
     # # Insert a row of data
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # # Save (commit) the changes
    # conn.commit()
    # # We can also close the connection if we are done with it.
    # # Just be sure any changes have been committed or they will be lost.
    # conn.close()


    # db = sqlite3.connect(database,
    #     detect_types=sqlite3.PARSE_DECLTYPES
    # )
    click.echo(f'Schema: {schema}')
    with open(schema) as f:
            s = f.read()
            # .decode('utf8')
            conn.executescript(s)
    conn.close()

if __name__ == '__main__':
    # cli()
    initdb()
    # init_db_command()            