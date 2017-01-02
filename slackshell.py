from slackclient import SlackClient
import os
import argparse
import ast
import random

SLACK_TOKEN = os.environ['SLACK_TOKEN']
sc = SlackClient(SLACK_TOKEN)

parser = argparse.ArgumentParser()

parser.add_argument("-a","--address", help="Address to where the message will be sent")
parser.add_argument("-c","--channel", help="Channel where the message will be sent")
parser.add_argument("-co","--count", help="Amount listed for file and message listing")
parser.add_argument("-cm","--comment", help="Comment for the file uploaded")
parser.add_argument("-l","--label", help="Label for the uploaded file")
parser.add_argument("-ls","--list", help="Lists all information that matches the query")
parser.add_argument("-m","--message", help="Input is the message that will be sent")
parser.add_argument("-p","--post",nargs=2,help="Channel where the message will be sent",
metavar=('MESSAGE','CHANNEL'))
parser.add_argument("-q","--query", help="Specifics for list. Possible args are 'info', 'members'")
parser.add_argument("-r","--receiver", help="Recipent where the message will be sent")
parser.add_argument("--reply", help="Reply to user who mentioned you last")
parser.add_argument("-s","--send", nargs=2, help="Channel where the message will be sent",
metavar=('MESSAGE','RECIPENT'))
parser.add_argument("-tp","--type", help="File type for file operations")
parser.add_argument("--update", help="Channel where the message will be sent")
parser.add_argument("-u","--upload", help="Upload files to a certain location")
parser.add_argument("-v","--view", help="View recent activity in a certain channel")

args = parser.parse_args()

message_cache = open(".message_cache.txt", 'a')

# helper functions
def channelToID(ch):
    if('#' in ch):
        nch = ch.replace('#','')
        ch = nch

    c = sc.api_call("channels.list")
    for n in c['channels']:
        if(ch in n['name']):
            return n['id']

def usernameToID(us):
    if(us[0] == "@"):
        n_us = us.replace("@","")
        return listUsers("np_id", n_us)
    else:
        return listUsers("np_id", us)

def idToUser(id):
    s = sc.api_call("users.list")
    sm = s['members']
    for x in range(0,len(sm)):
        if(sm[x]['id'] == id):
            return sm[x]['name']

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        f.close
    return i + 1

# messaging functions
def postMessage(ch,message):
    if(str(message).lower() != "null"):
        try:
            if(message[0] == '@'):
                temp = message[1:message.index(' ')]
                temp_id = usernameToID(temp)
                nt = message.replace(message[0:message.index(' ')],'<@' + temp_id + '|' + temp + '>')
                message = nt
        except:
            next
        s = sc.api_call("chat.postMessage", channel=ch, text=message)['message']
        message_cache.write(str(s) + "\n")
        print("Posted: '" + message + "' in " + ch)

def sendMessage(receiver,message):
    if(message[0] != '@'):
        temp = '@' + receiver
        receiver = temp
    if(str(args.message).lower != "null"):
        s = sc.api_call("chat.postMessage", channel=receiver,text=message)
        m = s['message']
        m['send_to'] = receiver
        message_cache.write(str(m) + "\n")
        print("Sent '" + message + "' to " + receiver)

# file functions
def fileUpload(fn,address,cm=None,ti=None):
    f = open(fn, 'r')
    if('#' in address):
        temp = address.replace('#','')
        address = temp
    try:
        if(cm == None):
            if(ti != None):
                s = sc.api_call("files.upload", file=f, filename=fn,
                channels=address,is_public="True",title=ti)
            else:
                s = sc.api_call("files.upload", file=f, filename=fn,
                channels=address,is_public="True")
        else:
            if(ti != None):
                s = sc.api_call("files.upload", file=f, filename=fn,
                channels=address,is_public="True",title=ti,initial_comment=cm)
            else:
                s = sc.api_call("files.upload", file=f, filename=fn,
                channels=address,is_public="True",initial_comment=cm)
    except:
        print("Error: Invalid channel(s)")
    print("Uploaded: '" + fn + "'")

# listing functions
def listChannels(query=None):
    s = sc.api_call("channels.list")['channels']
    l = ['']
    if(query == None):
        for key in s:
            print("#" + key['name'])
            l.append(key['name'])
        return l
    elif(query.lower() == "members"):
        for key in s:
            print("#" + key['name'])
            n = key['num_members']
            l.append(key['name'])
            p = 's'
            if(n == 1):
                p = ''
            print(str(n) + " member" + p)
        return l
    elif(query.lower() == "info"):
        for key in s:
            print("#" + key['name'])
            l.append(key['name'])
            d = key['topic']['value']
            if(d == ''):
                print("Channel contains no description")
            else:
                print(d)
        return l
    else:
        print("Error: " + "'" + query + "' is an invalid query")

def np_listChannels(query=None):
    s = sc.api_call("channels.list")['channels']
    l = ['']
    if(query == None):
        for key in s:
            l.append(key['name'])
        return l
    elif(query.lower() == "members"):
        for key in s:
            n = key['num_members']
            l.append(key['name'])
            p = 's'
            if(n == 1):
                p = ''
            print(str(n) + " member" + p)
        return l
    elif(query.lower() == "info"):
        for key in s:
            l.append(key['name'])
            d = key['topic']['value']
            if(d == ''):
                print("Channel contains no description")
            else:
                print(d)
        return l
    else:
        print("Error: " + "'" + query + "' is an invalid query")

def listEmoji():
    s = sc.api_call("emoji.list")
    for x in s['emoji']:
        print(x)

def listGroups():
    s = sc.api_call("groups.list")
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

def listUsers(query=None,address=None):
    s = sc.api_call("users.list")
    if(address != None):
        if(address[0] == '#'):
            temp = address.replace('#', '')
            address = temp
        if(not(address in np_listChannels()) and str(query).lower() != 'np_id'):
            print("Error: Invalid address")
            return
        elif(str(query).lower() != 'np_id'):
            address = channelToID(address)
            s = sc.api_call("channels.info",channel=address)
            for m in s['channel']['members']:
                print(idToUser(m))
            return
    if(str(query).lower() == "np_id"):
        for u in s['members']:
            m = u['name']
            if(address == m):
                return u['id']
    elif(str(query).lower() == "id"):
        for u in s['members']:
            m = u[query.lower()]
            print(m)
    elif(str(query).lower() == "rn"):
        for u in s['members']:
            m = u['real_name']
            print(m)
    elif(str(query).lower() == "email"):
        for u in s['members']:
            m = u['profile']
            try:
                print(m['name'] + ": " + m[str(query).lower()])
            except:
                print(m['real_name'] + ": ")
    elif(str(query).lower() == "phone"):
        for u in s['members']:
            m = u['profile']
            try:
                print(m['name'] + ": " + m[str(query).lower()])
            except:
                print(m['name'] + ": ")
    elif(str(query).lower() == "skype"):
        for u in s['members']:
            m = u['profile']
            try:
                print(m['name'] + ": " + m[str(query).lower()])
            except:
                print(m['name'] + ": ")
    elif(str(query).lower() == "fn"):
        for u in s['members']:
            m = u['profile']
            try:
                print(m['name'] + ": " + m['first_name'])
            except:
                print(m['name'] + ": ")
    elif(str(query).lower() == "ln"):
        for u in s['members']:
            m = u['profile']
            try:
                print(m['name'] + ": " + m['last_name'])
            except:
                print(m['name'] + ": ")
    elif(query == None or str(query).lower() == "name"):
        for u in s['members']:
            m = u['name']
            print(m)
    else:
        if(query != None):
            print("Error: Invalid query")
        else:
            print("Error: Invalid address")

def listReactions(us=None):
    if(us==None):
        s = sc.api_call("reactions.list")
        ts = ['']
        for x in s['items']:
            t = x['message']['ts']
            y = x['message']['reactions']
            for r in y:
                if(not(t in ts)):
                    for p in y:
                        print(p['name'])
                    ts.append(t)
    else:
        try:
            temp = us
            us = usernameToID(us)
            s = sc.api_call("reactions.list",user=us)
            reactions = ['']
            ts = ['']
            print("Reactions by: " + temp)
            for x in s['items']:
                t = x['message']['ts']
                y = x['message']['reactions']
                for r in y:
                    if(not(t in ts)):
                        for p in y:
                            reaction = p['name']
                            if(not(reaction in reactions)):
                                print(reaction)
                                reactions.append(reaction)
                        ts.append(t)
        except:
            print("Error: Invalid user")

def listFiles(_address=None,_type=None,_count=None,_user=None):
    if(_address != None):
        _address = channelToID(_address)
    if(_user != None):
        _user = usernameToID(_user)
        if(_user == None):
            print("Error: Invalid user")
            return
    if(_address != None):
        if(_user != None):
            if(_type != None):
                if(_count != None):
                    s = sc.api_call("files.list",channel=_address,types=_type,
                    count=_count,user=_user)
                else:
                    s = sc.api_call("files.list",channel=_address,types=_type,
                    user=_user)
            elif(_count != None):
                s = sc.api_call("files.list",channel=_address,count=_count,
                user=_user)
            else:
                s = sc.api_call("files.list",channel=_address,user=_user)
        else:
            if(_type != None):
                if(_count != None):
                    s = sc.api_call("files.list",channel=_address,types=_type,
                    count=_count)
                else:
                    s = sc.api_call("files.list",channel=_address,types=_type)
            elif(_count != None):
                s = sc.api_call("files.list",channel=_address,count=_count)
            else:
                s = sc.api_call("files.list",channel=_address)
    elif(_type != None):
        if(_count != None):
            s = sc.api_call("files.list",types=_type,count=_count)
        else:
            s = sc.api_call("files.list",types=_type)
    elif(_count != None):
        s = sc.api_call("files.list",count=_count)
    else:
        s = sc.api_call("files.list")
    links = []
    for x in s:
        f = s['files']
        for y in f:
            try:
                el = y['edit_link']
                temp = el.replace('/edit','')
                el = temp
                if(not(el in links)):
                    links.append(el)
                    print(el)
            except:
                next

def listSent(address=None):
    if(address == None):
        try:
            l = file_len('.message_cache.txt')
        except:
            l = 0
        p = ''
        if(l > 1 or l == 0):
            p = 's'

        print(str(l) + " message" + p + " sent")
        i = 1
        with open('.message_cache.txt') as f:
            for line in f:
                dl = ast.literal_eval(line)
                print("[" + str(i) + "][r:" + dl['send_to']+ "] " + dl['text'])
                i += 1

# history functions
def view(view_query,_count=None,np=False):
    try:
        temp = view_query
        if(view_query[0] == '#'):
            temp = view_query.replace('#','')
            view_query = temp
        view_query = channelToID(view_query)
    except:
        print("Channel not '" + view_query + "' not found")
        return
    if(_count == None):
        _count = 100
    s = sc.api_call("channels.history",channel=view_query,count=_count)

    stamps = []
    output = []
    for x in s:
        m = s['messages']
        for y in range(0,len(m)):
            t = m[y]['text']
            ts = m[y]['ts']
            try:
                u = idToUser(m[y]['user'])
                c = "[@" + u + "] " + t
            except:
                c = "[BOT] " + t
            if(not(ts in stamps)):
                stamps.append(ts)
                output.append(c)

    output.reverse()
    if(not(np)):
        print('#' + temp)
        for x in output:
            print(x)
    return output

def reply(reply,channel):
    posts = view(channel,10,True)
    user = sc.api_call("auth.test")['user']
    formatted_user = '<@' + usernameToID(user) + "> "
    for x in posts:
        if(formatted_user in x):
            left_bound = x.index('@') + 1
            right_bound = x.index(']')
            reply_user = x[left_bound:right_bound]
            formatted_reply = '<@' + usernameToID(reply_user) + "|" + reply_user + "> " + reply
            postMessage(channel,formatted_reply)
            break
# decides what functions to call
def delegate(args):
    if(args.post != None):
        try:
            postMessage(args.post[1], args.post[0])
        except:
            print("Error: Invalid channel")
    elif(args.send != None):
        try:
            sendMessage(args.send[1], args.send[0])
        except:
            print("Error: Invalid recipent")
    elif(args.update != None):
        e = "Error: Update must contain valid timestamp, channel, and message fields"
        updateMessage(args.time, args.channel, args.message)
    elif(args.list != None):
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
            if(args.channel != None or args.address != None):
                if(args.address == None):
                    args.address = args.channel
                listPins(args.address)
            else:
                print("Error: You must provide a valid channel")
        elif(str(args.list).lower() == "reactions"):
            if(args.address == None):
                listReactions()
            else:
                listReactions(args.address)
        elif(str(args.list).lower() == "users"):
            if(args.query != None):
                if(args.channel != None or args.address != None):
                    if(args.address == None):
                        args.address = args.channel
                    listUsers(args.query,args.address)
                else:
                    listUsers(args.query)
            else:
                if(args.channel != None or args.address != None):
                    if(args.address == None):
                        args.address = args.channel
                    listUsers(None,args.address)
                else:
                    listUsers()
        elif(str(args.list).lower() == "files"):
            if(args.channel != None or args.address != None):
                if(args.address == None):
                    args.address = args.channel
            listFiles(args.address,args.type,args.count,args.user)
        elif(str(args.list).lower() == "sent"):
            listSent()
        else:
            print("Unable to process listing")
    elif(args.upload != None):
        if(args.channel != None or args.address != None):
            if(args.address == None):
                args.address = args.channel
            fileUpload(args.upload,args.address,args.comment,args.label)
        else:
            print("Error: You must provide a channel or channels")
    elif(args.view != None):
        view(args.view,args.count)
    elif(args.reply != None):
        reply(args.reply,args.channel)
    else:
        print("Invalid command")

# initiates program
try:
    delegate(args)
except Exception as e:
    if(e.__class__.__name__ == 'TimeOutError'):
        print("Operation Timed Out; try again.")
    elif (e.__class__.__name__ == 'ConnectionError'):
        print("Unable to connect. Reconnect to your wifi and try again")
    else:
        print("You found an error. Darn. Let me know so I can fix it: jake.lawrence24@gmail.com")
        funny_videos = ['https://youtu.be/420eCJ7cKaE','https://youtu.be/vGyHXW0lwZY',
        'https://youtu.be/8PpXAPanaDU','https://youtu.be/V4MNbTGl0v4','https://youtu.be/bWhu0LovWgY',
        'https://youtu.be/m-1dApazt-U','https://youtu.be/_WyVZt77CM4']
        funny_video_link = funny_videos[random.randint(0,len(funny_videos)-1)]
        print("A funny video for your troubles: " + funny_video_link)
        print(str(e.__class__.__name__) + ": " + str(e))
# closes cache
message_cache.close()
