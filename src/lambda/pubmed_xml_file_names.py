import json

'''
Creates the list of filenames on the FTP server by eyeballing it.

One could also ftplib and LIST the contents, as well. This is simpler.

usage:

$ python pubmed_xml_file_names.py > pubmed_filenames.csv 

then from psql:

$ psql -h [db url] -d [database] -U [user]

[database] => \copy data_load(packet_name,downloaded_ind) from 'pubmed_filenames.csv' delimiter ',' CSV
'''

def handler(event, context):
    prefix='pubmed19n'
    postfix='.xml.gz,2'
    stop = event.get('stop') or 1525
    start = event.get('start') or 973
    x = start
    while x < stop + 1:
        print(prefix + numba(x) + postfix)
        x = x + 1
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def numba(n):
    ans = str(n)
    if n < 10:
        ans = '0' + ans
    if n < 100:
        ans = '0' + ans
    if n < 1000:
        ans = '0' + ans
    return ans

if __name__=='__main__':
    handler({ }, None)
