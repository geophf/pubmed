import psycopg2

from deployments.environment import db

# manages the db connection around database functions

def with_db_connection(db,fn):
    ans = None
    conn = None
    cursor = None
    try:
        (conn,cursor) = db_connector(*db)
        ans = fn(cursor)
        conn.commit()
    except Exception as error:
        print('Got an error',error)
    finally:
        db_disconnect(conn,cursor)
    return ans

def db_connector(dbms,db):
    conn = None
    print('Connecting to',dbms,db,'database')
    conn = psycopg2.connect(host=dbms,database=db,user='postgres',
                            password='s0maPr1m3')
    cursor = conn.cursor()
    return (conn,cursor)

def db_disconnect(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# a simple query service: the query is compact

def db_query(cursor,stmt):
    cursor.execute(stmt)
    ans = None
    if cursor.rowcount > 0:
        ans = cursor.fetchall()
    return ans

def fetch_lookup_table(cursor,table):
    print('Fetching lookup table',table,'data')
    ans = { }
    cursor.execute('SELECT * from ' + table)
    for row in cursor.fetchall():
        ans[row[1]] = row[0]
    return ans

# but what if the table doesn't 'play nice'?

def fetch_dictionary(cursor,column,table):
    print('Fetching all ' + column + '-values in ' + table)
    cursor.execute('SELECT ' + column + ',id FROM ' + table)
    dict = { }
    rows = cursor.fetchall()
    for row in rows:
        dict[row[0]] = row[1]
    print('Fetched',len(dict),table)
    return dict

# now we want to look up a value ... is it there?

def lookup_or_add(cursor,table,col,val,dict):
    ans = dict.get(val)
    if not ans:
        stmt='INSERT INTO ' + table + ' (' + col + ') VALUES (%s) RETURNING id'
        cursor.execute(stmt,(val,))
        ans = cursor.fetchone()[0]
        dict[val] = ans
    return (ans,dict)

def fetch_or_add(cursor,table,col,val):
    lk = fetch_lookup_table(cursor,table)
    return lookup_or_add(cursor,table,col,val,lk)[0]

def build_then_insert(cursor,table,kvs):
    s0 = 'INSERT INTO ' + table + '('
    cols = ','.join(kvs.keys())
    stmt = s0 + cols + ') VALUES (%s) RETURNING id'
    cursor.execute(stmt,(tuple(kvs.values()),))
    return cursor.fetchone()[0]

# pivot/join table 

def pivot_on(table,cols,cursor,src,dests):
    print('Adding',len(dests),'pivot rows to',table,'for id',src)
    stmt='INSERT INTO '+table+' (' + ','.join(cols) + ') VALUES (%s,%s)'
    for dest in dests:
        cursor.execute(stmt,(src,dest))

# ----- TEST FUNCTION --------------------------------------------------

def sample_run(cursor):
    cursor.execute('select * from duality_lk LIMIT 10')
    for row in cursor.fetchall():
        print(row)

if __name__ == '__main__':
    with_db_connection(db, sample_run)
