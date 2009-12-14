#!/usr/bin/python

from __future__ import with_statement
import sys, time
import urllib

import sms
import wiki

def get_requests():
    requests = []
    for msg in sms.receive():
        requests.append(dict(
                src=msg['phoneNumber'], 
                txt=msg['text'], 
                t=int(time.mktime(msg['startTime']))-28800))
    return requests

def moses(requests):
    reads = [r for r in requests if r['txt'].find(' ') == -1]
    writes = [r for r in requests if r['txt'].find(' ') != -1]
    return reads, writes

def do_write(write, wiki):
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

def do_read(read, wiki):
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
        sms.send(src, '### Not found')

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


def main(args):
    wiki.init()

    wikidata = wiki.load()

    print "Running..."
    while True:
        requests = get_requests()
        if len(requests):
            print "Got %s requests: " % len(requests), requests
        reads, writes = moses(requests)

        # process writes before reads so readers get the latest data
        for write in writes:
            do_write(write, wikidata)
            
        wiki.dump(wikidata)

        for read in reads:
            do_read(read, wikidata)

        time.sleep(3)

if __name__ == '__main__':
    import sys
    main(sys.argv)
