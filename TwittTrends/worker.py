from time import sleep


import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1
from concurrent.futures import ThreadPoolExecutor


arn = 'arn:aws:sns:us-east-1:332176844987:TwittTrends'
queueName = 'TwittTrends'
alchemyapi = AlchemyLanguageV1(api_key='bb4bc7f058004c73d08b9983fc76e84af3701e0f')

thread_waittime =  10
working = 10

sqs = boto3.resource('sqs')
sns = boto3.resource('sns')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/332176844987/TwittTrends')
endpoint = sns.PlatformEndpoint(arn)




def parse_tweet():
    print("sleep")
    #sleep(working)
    print("done sleep")
    for message in queue.receive_messages(MessageAttributeNames=['All'], VisibilityTimeout=30, MaxNumberOfMessages=1):
        print("moo")
        if message.body is not None:
            print(message.body)
            tweet_json = json.loads(message.body)
            print("moo1")
            snsMsg = {}
            ## geo
            coordinates = tweet_json['coordinates']
            tweet_text = tweet_json['text']
            print(tweet_text)
            response = alchemyapi.sentiment(text=tweet_text)
            print(response)
            if response['status'] == 'OK':

                sentimentResult = response["docSentiment"]

                snsMsg['sentiment'] = sentimentResult
                snsMsg['tweet'] = message.body
                snsMsg['coordinates'] = coordinates
                ## dump snsMsg and send message to SNS
                snsMessage = json.dumps(snsMsg)
                print(snsMsg['sentiment'])
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
