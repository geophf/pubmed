import gzip
import urllib.request
import io

from pubmed_xml_gz_scanner import scan_file

def handler(event,context):
   url = event.get('url')
   response = urllib.request.urlopen(url)
   compressed_file = io.BytesIO(response.read())
   decompressed_file = gzip.GzipFile(fileobj=compressed_file)
   some_more = decompressed_file.read()
   scan_file(some_more)

if __name__== '__main__':
   evt = { }
   evt['url'] = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/pubmed19n1523.xml.gz'
   handler(evt,None)
