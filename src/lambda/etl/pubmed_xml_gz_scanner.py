import gzip
import xml.etree.ElementTree as ET

# reads in a compressed XML file for storage in DB

def handler(event,context):
   filename = event.get('filename')
   if filename:
      print('For file',filename)
      input = gzip.open(filename, 'r')
      scan_file(input)
   else:
      print('no filename to scan')

def scan_file(cursor,pack_id,file,yn_lk):
   print('converting file to xml')
   root = ET.fromstring(file)

   # print(root.tag) # prints PubmedArticleSet
   # print(root.attrib) # prints {}
   arts = 0
   for art in root.iter('PubmedArticle'):
      arts = arts + 1
      store_art_xml(cursor,pack_id,art,yn_lk)
      if arts % 500 == 0:
         print('Stored',arts,'articles')
   print('There are',arts)
   return { 'abstracts': arts }

def store_art_xml(cursor,pack_id,art,yn_lk):
   stmt='''
INSERT INTO abstract_stg (packet_id,raw_xml,parsed_ind) 
VALUES (%s,%s,%s)
RETURNING id
'''
   xml_to_store = ET.dump(art)
   cursor.execute(stmt,(pack_id,xml_to_store,yn_lk['N']))


if __name__ == '__main__':
   evt = { }
   evt['filename'] = 'pubmed19n0972.xml.gz'
   handler(evt,None)
