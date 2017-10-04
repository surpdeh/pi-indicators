import re
import time
import json
from slackclient import SlackClient

def connectSlack(config):
    """Connect to slack with given configuration and return connected client and user ID"""
    slack_client = SlackClient(config['apikey'])
    # Fetch the Bot's User ID

    user_list = slack_client.api_call("users.list")
    for user in user_list.get('members'):
        if user.get('name') == config['username']:
            slack_user_id = user.get('id')
            break


    # Start connection
    if slack_client.rtm_connect():
        print "Connected!"

    return (slack_client, slack_user_id)


def startProducer(slack_connection, eventHandler):
    """A function to read events and invoke eventHandler. Does not return"""
    (client, userId) = slack_connection
    
    while True:
        for message in client.rtm_read():
            if 'text' in message: # and message['text'].startswith("<@%s>" % userId):

                print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text'] #.\
                    #split("<@%s>" % userId)[1].\
                    #strip()

                eventHandler(message_text)

    # never get here
    return

def writeback(slack_client):
    slack_client.api_call(
        "chat.postMessage",
        channel=message['channel'],
        text="Lights are now on",
        as_user=True)

    return

if __name__ == "__main__":
    import sys
    print "Should have a test harness here"
