import json

def lambda_handler(event, context):
    prefix='pubmed19n'
    postfix='.xml.gz,2'
    x = 1
    while x < 973:
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
    lambda_handler(None, None)
