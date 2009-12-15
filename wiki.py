from __future__ import with_statement
import simplejson
import time

from shortnet import ERROR_MARK
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
    t = int(write['t'])

    idx = write['txt'].find(' ')
    page = write['txt'][:idx]
    content = write['txt'][idx+1:]
    
    # Check append flag
    if page.endswith('+'):
        page = page[:-1]
        append_flag = True
    else:
        append_flag = False
    
    # Check if a profile page
    potential_profile_page = sms.extend_number(src, page)
    if potential_profile_page in wiki and potential_profile_page != src:
        sms.send(src, "### Not authorized")
        print "Unauthorized write attempt on '%s' from %s." % (page, src)
        return
    elif potential_profile_page == src:
        page = potential_profile_page
    
    # Append modifier
    if append_flag and page in wiki:
        content = ' '.join([wiki[page]['content'], content])
    
    wiki[page] = {
        'page': page,
        'content': content,
        'author': src,
        'mtime': t,}
        
    sms.send(src, "%s %s/%s" % (content, sms.localize_number(src, src), time_ago(t)))
    print "Write on page '%s' from %s." % (page, src)

def read(read, wiki):
    src = read['src']
    t = read['t']
    page = read['txt']

    if sms.extend_number(src, page) in wiki:
        page = sms.extend_number(src, page)

    if page in wiki:
        entry = wiki[page]
        content = entry['content']
        author = entry['author']
        sms.send(src, "%s %s/%s" % (content, sms.localize_number(author, src), time_ago(entry['mtime'])))
        print "Read on page '%s' from %s." % (page, src)
    else:
        print "Read on unknown page '%s' from %s." % (page, src)
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