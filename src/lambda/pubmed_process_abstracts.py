from common.db import with_db_connection
from deployments.environment import db

def handler(event, context):
   return with_db_connection(db, process_packet)

def process_packet(cursor):
   da_sql='''
SELECT dl.id,dl.packet_name
FROM data_load dl
JOIN duality_lk d ON d.id=dl.downloaded_ind
WHERE d.truth_serum='N'
LIMIT 1'''

   cursor.execute(da_sql)
   ans = { 'result': 'no packets to process' }
   if cursor.rowcount > 0:
      ans = due_process(cursor)
   return ans

def due_process(cursor):
   row = cursor.fetchone()
   pn = row[1]
   id = row[0]
   print('processing packet',pn,'id:',id)
   return { pn : id }
