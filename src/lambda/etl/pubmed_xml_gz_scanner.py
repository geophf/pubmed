import gzip
from lxml import etree
from io import BytesIO

# reads in a compressed XML file for storage in DB

def handler(event,context):
   filename = event.get('filename')
   if filename:
      print('For file',filename)
      zippy = gzip.GzipFile(filename)
      zappy = zippy.read()
      scan_file(None,1,zappy,None)
   else:
      print('no filename to scan')

def scan_file(cursor,pack_id,strg,yn_lk):
   print('converting file to xml')
   print('length of file is',len(strg))

   arts = 0
   str1 = BytesIO(strg)
   conn = cursor.connection
   print('number of abstracts:',arts)
   for _,art in etree.iterparse(str1, tag='PubmedArticle'):
      arts = arts + 1
      store_art_xml(cursor,pack_id,art,yn_lk)
      if arts % 2500 == 0:
         print('Stored',arts,'articles')
         conn.commit()
      art.clear()
   print('There are',arts)
   return { 'abstracts': arts }

def store_art_xml(cursor,pack_id,art,yn_lk):
   stmt='''
INSERT INTO abstract_stg (packet_id,raw_xml,parsed_ind) 
VALUES (%s,%s,%s)
RETURNING id
'''
   xml_to_store = etree.tostring(art).decode('utf-8')
   cursor.execute(stmt,(pack_id,xml_to_store,yn_lk['N']))

if __name__ == '__main__':
   evt = { }
   evt['filename'] = 'pubmed19n0972.xml.gz'
   handler(evt,None)
