from common.db import with_db_connection,fetch_lookup_table
from deployments.environment import db

from pubmed_gz_downloader import download_and_scan_packet

def handler(event, context):
   return with_db_connection(db, loop)

def loop(cursor):
   get_more = 0 == 0
   errors = 0
   while get_more and errors < 5:
      ans = process_packet(cursor)
      get_more = not ans.get('result')
      if ans.get('error'):
         errors = errors + 1
   print('done.')
   print('There were',errors,'errors.')

def process_packet(cursor):
   yn_lk = fetch_lookup_table(cursor,'duality_lk')
   da_sql='''
SELECT id,packet_name
FROM data_load
WHERE downloaded_ind=%s
LIMIT 1'''

   cursor.execute(da_sql,(yn_lk['N'],))
   ans = { 'result': 'no packets to process' }
   if cursor.rowcount > 0:
      ans = due_process(cursor,yn_lk)
      cursor.connection.commit()
   return ans

def due_process(cursor,yn_lk):
   row = cursor.fetchone()
   pn = row[1]
   id = row[0]
   print('processing packet',pn,'id:',id)
   ans = { 'packet': pn, 'id': id }
   try:
      scanned = download_and_scan_packet(cursor,id,pn,yn_lk)
      close_out_row(cursor,id,yn_lk)
      ans['scanned'] = scanned
   except Exception as err:
      ans['error'] = err
      bad_packet(cursor,id,err,yn_lk)
   return ans

def close_out_row(cursor,id,yn_lk):
   print('packet',id,'processed; committing')
   stmt='''
UPDATE data_load
SET downloaded_ind=%s,downloaded_dttm=now(),processed_ind=%s
WHERE id=%s
'''
   yup = yn_lk['Y']
   cursor.execute(stmt,(yup,yup,id))

def bad_packet(cursor,id,err,yn_lk):
   print('Got error',err,'for packet',id,'... logging.')
   stmt='''
UPDATE data_load
SET downloaded_ind=%s,downloaded_dttm=now(),processed_ind=%s,processing_error=%s
WHERE id=%s
'''
   yup = yn_lk['Y']
   nupe = yn_lk['N']
   cursor.execute(stmt,(yup,nupe,str(err),id))

if __name__=='__main__':
   print(handler(None,None))
