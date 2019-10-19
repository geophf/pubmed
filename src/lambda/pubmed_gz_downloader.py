import gzip
import urllib.request
import io

from pubmed_xml_gz_scanner import scan_file

ftp_url='ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/'

def handler(event,context):
   packet = event.get('packet')
   return download_and_scan_packet(packet)

def download_and_scan_packet(packet):
   print('Downloading',packet,'from',ftp_url)
   url = ftp_url + packet
   response = urllib.request.urlopen(url)
   compressed_file = io.BytesIO(response.read())
   decompressed_file = gzip.GzipFile(fileobj=compressed_file)
   some_more = decompressed_file.read()
   return scan_file(some_more)

if __name__== '__main__':
   evt = { }
   evt['packet'] = 'pubmed19n1523.xml.gz'
   handler(evt,None)
