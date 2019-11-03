from common.db import with_db_connection
from deployments.environment import db

# queries the status of a data load

def handler(event, context):
   print('Querying data load')
   raw = with_db_connection(db, query_db)
   return xform(raw)

def query_db(cursor):
   stmt='''
select b.truth_serum as downloaded,count(a.downloaded_ind) as cnt 
from data_load a
join duality_lk b on a.downloaded_ind=b.id
group by b.truth_serum;
'''
   cursor.execute(stmt)
   return cursor.fetchall()

def xform(rows):
   ans = { }
   xlate = { 'Y': 'downloaded', 'N': 'not_downloaded' }
   for row in rows:
      ans[xlate[row[0]]] = row[1]
   return ans

if __name__=='__main__':
   print(handler(None,None))
