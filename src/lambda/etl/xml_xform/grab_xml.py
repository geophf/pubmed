from deployments.environment import db,parse_xml_arn

from common.db import with_db_connection,fetch_lookup_table
from common.sns import ping_arn

from parse_xml import parse_row
from store_xml import store_row

# we extract a row of raw xml, then hand it off to be processed, storing the
# results back into the database, but now in a relational model.

def handler(event, context):
   print('grabbing a row for processing')
   return with_db_connection(db, grab_row)

def grab_row(cursor):
   yn_lk=fetch_lookup_table(cursor,'duality_lk')
   stmt='''
SELECT id,raw_xml
FROM abstract_stg
WHERE parsed_ind=%s
AND parsing_error IS NULL
LIMIT 1
'''
   ans = { 'parsed' : 'Nothing to parse' }
   cursor.execute(stmt,(yn_lk['N'],))
   if cursor.rowcount > 0:
      row = cursor.fetchone()
      row_id = row[0]
      row_xml = row[1]
      try:
         skml = parse_row(row_id,row_xml)
         store_row(cursor,row_id,skml,yn_lk)
         update_staging_table(cursor,row_id,yn_lk)
         ping_arn(parse_xml_arn)
      except Exception as err:
         str_err = str(err)
         ans['error'] = str_err
         report_error(cursor,row_id,str_err)
   else:
      print('No row to process. Done.')
   return ans

def update_staging_table(cursor,row_id,yn_lk):
   print('closing out row',row_id,'as parsed in staging table')
   stmt='''
UPDATE abstract_stg
SET parsed_ind=%s,parsed_dttm=now()
WHERE id=%s
'''
   cursor.execute(stmt,(yn_lk['Y'],row_id))

def report_error(cursor,row_id,str_err):
   print('Got error when processing row',row_id,'error:',str_err)
   stmt='''
UPDATE abstract_stg
SET parsing_error=%s,parsed_dttm=now()
WHERE id=%s
'''
   cursor.execute(stmt,(str_err,row_id))

if __name__=='__main__':
   print(handler(None,None))
