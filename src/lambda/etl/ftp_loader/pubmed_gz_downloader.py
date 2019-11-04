import gzip
from ftplib import FTP
import io

from pubmed_xml_gz_scanner import scan_file

sio = io.BytesIO()
ftp_url='ftp.ncbi.nlm.nih.gov'
wd = '/pubmed/updatefiles/'

def handler(event,context):
   packet = event.get('packet')
   return download_and_scan_packet(packet)

def handle_binary(more_data):
    sio.write(more_data)

def download_and_scan_packet(cursor,pack_id,packet,yn_lk):
   print('Downloading',packet,'from',ftp_url)
   ftp = FTP(ftp_url)
   ftp.login() # Username: anonymous password: anonymous@

   resp = ftp.retrbinary("RETR " + wd + packet, callback=handle_binary)
   print('retrieved binary data')
   sio.seek(0) # Go back to the start
   print('Soaked')
   zippy = gzip.GzipFile(fileobj=sio)
   print('Unzipped')
   uncompressed = zippy.read()
   print('read')

   print('The first 100 or so characters of',packet,'are',uncompressed[0:100])
   ans = scan_file(cursor,pack_id,uncompressed,yn_lk)
   
   # now let's clear out the io-cache for our next run-thru
   sio.truncate(0)
   sio.seek(0)
   return ans

if __name__== '__main__':
   evt = { }
   evt['packet'] = 'pubmed19n1523.xml.gz'
   handler(evt,None)
