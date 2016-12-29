from slackclient import SlackClient
import os
import argparse

SLACK_TOKEN = os.environ['SLACK_TOKEN']
sc = SlackClient(SLACK_TOKEN)

parser = argparse.ArgumentParser()
parser.add_argument("-p","--post", help="Channel where the message will be sent")
parser.add_argument("-s","--send", help="Channel where the message will be sent")
parser.add_argument("-u","--update", help="Channel where the message will be sent")
parser.add_argument("--history", help="Get messages that match a certain query")
parser.add_argument("-ls","--list", help="Lists all information that matches the query")
parser.add_argument("-c","--channel", help="Channel where the message will be sent")
parser.add_argument("-r","--receiver", help="Recipent where the message will be sent")
parser.add_argument("-a","--address", help="Address to where the message will be sent")
parser.add_argument("-m", "--message", help="Input is the message that will be sent")
parser.add_argument("-t", "--time", help="Timestamp of the message that wants to be updated")
parser.add_argument("-q", "--query", help="Specifics for list. Possible args are 'info', 'members'")

args = parser.parse_args()

message_cache = open("cache/message_cache.txt", 'a')

# helper functions
def channelToID(ch):
    if('#' in ch):
        nch = ch.replace('#','')

    c = sc.api_call("channels.list")
    for n in c['channels']:
        if(nch in n['name']):
            return n['id']

# messaging functions
def postMessage(ch,message):
    if(str(args.message).lower() != "null"):
        s = sc.api_call("chat.postMessage", channel=ch, text=message)['message']
        message_cache.write(str(s) + "\n")
        print("Posted: '" + message + "' in " + ch)

def sendMessage(receiver,message):
    if(str(args.message).lower != "null"):
        s = sc.api_call("chat.postMessage", channel=receiver,text=message)['message']
        message_cache.write(str(s) + "\n")
        print("Sent '" + message + "' to " + receiver)

def updateMessage(time,channel,message):
    print("f")

# listing functions
def listChannels(query=None):
    s = sc.api_call("channels.list")['channels']
    if(query == None):
        for key in s:
            print("#" + key['name'])
    elif(query.lower() == "members"):
        for key in s:
            print("#" + key['name'])
            n = key['num_members']
            p = 's'
            if(n == 1):
                p = ''
            print(str(n) + " member" + p)
    elif(query.lower() == "info"):
        for key in s:
            print("#" + key['name'])
            d = key['topic']['value']
            if(d == ''):
                print("Channel contains no description")
            else:
                print(d)
    else:
        print("Error: " + "'" + query + "' is an invalid query")

def listEmoji():
    s = sc.api_call("emoji.list")
    for x in s['emoji']:
        print(x)

def listGroups(query=None):
    s = sc.api_call("groups.list")
    if(query == None):
        for x in s['groups']:
            print("#" + x['name'])
def listDM():
    s = sc.api_call("im.list")
    p = sc.api_call("users.list")
    users = ['']
    names = ['']
    for x in s['ims']:
        users.append(x['user'])
    for m in p['members']:
        if(m['id'] in users):
            names.append(m['real_name'])
    for n in range(1,len(names)):
        print(names[n])

def listPins(ch):
    ch = channelToID(ch)
    s = sc.api_call("pins.list", channel=ch)
    for p in s['items']:
        print(p['message']['username'] + ": " + p['message']['text'])

# history functions
def getHistory(id,channel):
    print("WIP")

# decides what functions to call
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
    elif(args.history != None):
        if(args.channel != None):
            try:
                getHistory(args.history,args.channel)
            except:
                print("Error: Invalid ID or Channel")
    elif(args.update != None):
        e = "Error: Update must contain valid timestamp, channel, and message fields"
        updateMessage(args.time, args.channel, args.message)
    elif(args.list.lower() != None):
        if(str(args.list).lower() == "channels"):
            if(args.query != None):
                listChannels(args.query)
            else:
                listChannels()
        elif(str(args.list).lower() == "emoji"):
            listEmoji()
        elif(str(args.list).lower() == "groups"):
            listGroups()
        elif(str(args.list).lower() == "dm"):
            listDM()
        elif(str(args.list).lower() == "pins"):
            if(args.channel != None):
                listPins(args.channel)
            else:
                print("Error: You must provide a valid channel")

# initiates program
delegate(args)
# closes cache
message_cache.close()
