from time import sleep


import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1
from pyes import *
from concurrent.futures import ThreadPoolExecutor


arn = 'arn:aws:sns:us-east-1:332176844987:TwittTrends'
queueName = 'TwittTrends'
alchemyapi = AlchemyLanguageV1(api_key='bb4bc7f058004c73d08b9983fc76e84af3701e0f')

thread_waittime =  15
working = 20

sqs = boto3.resource('sqs')
sns = boto3.resource('sns')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=queueName)
endpoint = sns.PlatformEndpoint(arn)



tweet_count = 0

def parse_tweet():

    tweet_count += 1
    sleep(working)

    for message in queue.receive_messages(MessageAttributeNames=['All'], VisibilityTimeout=30, MaxNumberOfMessages=1):

        if message.message_attributes is not None:

            snsMsg = {}
            ## geo
            coordinates = message.message_attributes.get('coordinates').get('StringValue')
            if coordinates:
                ## sentiment

                tweet_text = message.body
                response = alchemyapi.sentiment(text=tweet_text)

                if response['status'] == 'OK':

                    sentimentResult = response["docSentiment"]

                    snsMsg['sentiment'] = sentimentResult
                    snsMsg['tweet'] = message.body
                    snsMsg['coordinates'] = coordinates
                    ## dump snsMsg and send message to SNS
                    snsMessage = json.dumps(snsMsg)
                    response = endpoint.publish(Message=snsMessage,Subject='TwittTrends')

        # Let the queue know that the message is processed
        message.delete()



def main():
    executor = ThreadPoolExecutor(max_workers=7)
    while True:
        executor.submit(parse_tweet)
        sleep(thread_waittime)

if __name__ == '__main__':
    main()
