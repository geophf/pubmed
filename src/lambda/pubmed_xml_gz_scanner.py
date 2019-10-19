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

def scan_file(file):
      root = ET.fromstring(file)
      # root = tree.getroot()

      print(root.tag)
      print(root.attrib)
      arts = 0
      for art in root.iter('PubmedArticle'):
         arts = arts + 1
      print('There are',arts)
      return { 'abstracts': arts }

if __name__ == '__main__':
   evt = { }
   evt['filename'] = 'pubmed19n0972.xml.gz'
   handler(evt,None)
