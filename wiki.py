from __future__ import with_statement
import simplejson
import time

from shortwiki import ERROR_MARK
import sms

WIKI_FILE = 'wiki.json'

def init():
    import os
    if not os.path.exists(WIKI_FILE):
        wiki = {}
        dump(wiki)

def load():
    with open(WIKI_FILE, 'r') as f:
        wiki = simplejson.load(f)
    return wiki

def dump(wiki):
    with open(WIKI_FILE, 'w') as f:
        simplejson.dump(wiki, f)
        f.write("\n")

def write(write, wiki):
    src = write['src']
    t = write['t']
    txt = write['txt']

    idx = txt.find(' ')
    page = txt[:idx]
    content = txt[idx+1:]
    wiki[page] = {
        'page': page,
        'content': content,
        'author': src,
        'mtime': int(t)}
    print "Write on page '%s' from %s." % (page, src)

def read(read, wiki):
    src = read['src']
    t = read['t']
    txt = read['txt']
    page = txt

    if txt in wiki:
        entry = wiki[page]
        content = entry['content']
        author = entry['author']
        sms.send(src, "%s %s/%s" % (content, author, time_ago(entry['mtime'])))
        print "Read on page '%s' from %s." % (txt, src)
    else:
        print "Read on unknown page '%s' from %s." % (txt, src)
        sms.send(src, '%s Not found' % ERROR_MARK)

def time_ago(from_time):
    seconds = int(time.time()) - from_time
    if seconds < 60:
        return "%ds" % int(seconds)
    if seconds < 3600:
        return "%dm" % int(seconds/60)
    if seconds < 86400:
        return "%dh" % int(seconds/3600)
    if seconds < 2629743.83:
        return "%dd" % int(seconds/86400)
    if seconds < 31556929:
        return "%dmo" % int(seconds/2629743.83)
    else:
        return "%dyr" % int(seconds/31556929)