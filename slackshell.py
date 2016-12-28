from slackclient import SlackClient
import os
import argparse

SLACK_TOKEN = os.environ['SLACK_TOKEN']
sc = SlackClient(SLACK_TOKEN)

parser = argparse.ArgumentParser()
parser.add_argument("--post", help="Channel where the message will be sent")
parser.add_argument("--send", help="Channel where the message will be sent")
parser.add_argument("--update", help="Channel where the message will be sent")
parser.add_argument("-c","--channel", help="Channel where the message will be sent")
parser.add_argument("-r","--receiver", help="Recipent where the message will be sent")
parser.add_argument("-a","--address", help="Address to where the message will be sent")
parser.add_argument("-m", "--message", help="Input is the message that will be sent")
parser.add_argument("-t", "--time", help="Timestamp of the message that wants to be updated")

args = parser.parse_args()

message_cache = open("cache/message_cache.txt", 'a')

def postMessage(ch,message):
    if(args.message != "null"):
        s = sc.api_call("chat.postMessage", channel=ch, text=message)
        message_cache.write(str(s) + "\n")
        print("Posted: '" + message + "' in " + ch)

def sendMessage(receiver,message):
    if(args.message != "null"):
        s = sc.api_call("chat.postMessage", channel=receiver,text=message)
        message_cache.write(str(s) + "\n")
        print("Sent '" + message + "' to " + receiver)

def updateMessage(time,channel,message):
    print("f")

def delegate(args):
    if(args.post != None):
        if(args.channel != None):
            args.address = args.channel
        try:
            postMessage(args.address, args.post)
        except:
            print("Error: Invalid channel")
    elif(args.send != None):
        if(args.receiver != None):
            args.address = args.receiver
        try:
            sendMessage(args.address, args.send)
        except:
            print("Error: Invalid recipent")
    elif(args.update != None):
        e = "Error: Update must contain valid timestamp, channel, and message fields"
        sendMessage(args.time, args.channel, args.message)
    return

delegate(args)
message_cache.close()
