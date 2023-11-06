

def DROP_TABLE(cur, table):
    cur.execute(f'DROP TABLE IF EXISTS {table}')
