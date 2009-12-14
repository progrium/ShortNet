from googlevoice import Voice
import BeautifulSoup

voice = Voice()
voice.login()

# by John Nagle
#   nagle@animats.com
def extractsms(htmlsms) :
    msgitems = []
    tree = BeautifulSoup.BeautifulSoup(htmlsms)	
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations:
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows:
            msgitem = {"id" : conversation["id"]}
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans:
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()
            msgitems.append(msgitem)
    return msgitems

def receive():
    voice.sms()
    msg_body = {}
    msg_meta = [m for m in voice.sms().messages if not m.isRead]
    for m in extractsms(voice.sms.html):
        msg_body[m['id']] = m
    for m in msg_meta:
        if m.id in msg_body:
            msg = dict(m)
            msg.update(msg_body[m.id])
            yield msg
            m.delete()

def send(to, message):
    voice.send_sms(to, message)