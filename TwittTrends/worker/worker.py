from time import sleep
import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1
from concurrent.futures import ThreadPoolExecutor
import boto.sqs
from boto.sqs.message import Message

arn = 'arn:aws:sns:us-east-1:332176844987:TwittTrends'
queueName = 'TwittTrends'
alchemyapi = AlchemyLanguageV1(api_key='bb4bc7f058004c73d08b9983fc76e84af3701e0f')

thread_waittime =  10
working = 10

# SNS
sns = boto3.resource('sns')
endpoint = sns.PlatformEndpoint(arn)
# SQS
conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='AKIAJ2SBRP7FL2443UCA', aws_secret_access_key='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')
queue = conn.create_queue('TwittTrends')

def parse_tweet():
    sleep(working)
    for message in queue.get_messages(1):
        if message.get_body() is not None:
            tweet_json = json.loads(message.get_body())
            snsMsg = {}
            ## parse tweet for location, text, and sentiment
            coordinates = tweet_json['coordinates']
            tweet_text = tweet_json['text']
            response = alchemyapi.sentiment(text=tweet_text)
            if response['status'] == 'OK':

                sentimentResult = response["docSentiment"]

                snsMsg['sentiment'] = sentimentResult
                snsMsg['tweet'] = tweet_text
                snsMsg['coordinates'] = coordinates
                # Dump snsMsg and send message to SNS
                snsMessage = json.dumps(snsMsg)
                print(snsMessage)
                response = endpoint.publish(Message=snsMessage,Subject='TwittTrends')
        # Let the queue know that the message is processed
        message.delete()

def main():
    parse_tweet()
    executor = ThreadPoolExecutor(max_workers=7)
    while True:
        executor.submit(parse_tweet)
        sleep(thread_waittime)

if __name__ == '__main__':
    main()
