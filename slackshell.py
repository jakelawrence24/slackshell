from slackclient import SlackClient
import os
import argparse

SLACK_TOKEN = os.environ['SLACK_TOKEN']
sc = SlackClient(SLACK_TOKEN)

parser = argparse.ArgumentParser()
parser.add_argument("intent", help="Determines what commands to execute. " +
"Valid commands include:\n\tpost\nwip")
parser.add_argument("-c","--channel", help="Channel where the message will be sent")
parser.add_argument("-r","--receiver", help="Channel where the message will be sent")
parser.add_argument("-m", "--message", help="Input is the message that will be sent")
parser.add_argument("-t", "--time", help="Timestamp of the message that wants to be updated")
parser.add_argument("-u", "--update", help="Input is the message that will be sent")
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
    #try:
    if(args.intent == "post"):
        e = "Error: Post must contain channel and message fields"
        postMessage(args.channel,args.message)
    if(args.intent == "send"):
        e = "Error: Content must contain channel and message fields"
        sendMessage(args.receiver, args.message)
    if(args.intent == "update"):
        e = "Error: Update must contain valid timestamp, channel, and message fields"
        sendMessage(args.time, args.channel, args.message)
    #except:
        #print(e)

delegate(args)
message_cache.close()
