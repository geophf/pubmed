import boto3
import json

# sends a message to an SNS topic (SNS: simple notification service)

from deployments.environment import region

sns = boto3.client(service_name="sns", region_name=region)

def send_message(arn,json_msg):
   print('Sending',json_msg,'to',arn)
   trip_it = json.dumps(json_msg)
   # print('Sending',trip_it,'for anaylsis')
   sns.publish(TopicArn=arn,Message=trip_it)

def ping_arn(arn):
   send_message(arn,{'hello':'world'})

# processes notifications from the SNS

def process_notification(notification):
   # we need to extract the message information from the SNS

   recs = notification.get('Records')
   ans = []
   if recs:
      ans = proc_notes(recs)
   return ans

def proc_notes(recs):
   nr = 0
   msgs = []
   for rec in recs:
      nr = nr + 1
      print('Processing notification',nr)
      evt = { }
      bod = rec.get('Sns')
      if bod:
         msg = bod.get('Message')
         if msg:
            # print('msg string is',msg)
            try:
               evt=json.loads(msg)
               msgs.append(evt)
            except Exception as err:
               # if an empty notifification, just call fetch_packet
               print('Received an empty notification',nr,'error:',err)

   return msgs
