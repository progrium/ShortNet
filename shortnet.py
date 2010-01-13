#!/usr/bin/python

import sys, time
import urllib

import sms
import wiki

ERROR_MARK = "###"

def get_requests():
    requests = []
    for msg in sms.receive():
        if not msg['text'].startswith(ERROR_MARK):
            requests.append(dict(
                src=msg['phoneNumber'], 
                txt=msg['text'], 
                t=int(time.mktime(msg['startTime']))-28800))
    return requests

def moses(requests):
    reads = [r for r in requests if r['txt'].find(' ') == -1]
    writes = [r for r in requests if r['txt'].find(' ') != -1]
    return reads, writes

commands = {}
def set_command(cmd, req):
    args = cmd.split(' ')
    if len(args) > 1:
        commands[args[0]] = args[1]
    sms.send(req['src'], "Command created")

def run_command(cmd, req):
    sms.send(req['src'], urllib.urlopen(commands[cmd]).read())

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
            if write['txt'].startswith('!'):
                set_command(write['txt'][1:], write)
            else:
                wiki.write(write, wikidata)
            
        wiki.dump(wikidata)

        for read in reads:
            if read['txt'].startswith('!'):
                run_command(read['txt'][1:], read)
            else:
                wiki.read(read, wikidata)

        time.sleep(3)

if __name__ == '__main__':
    import sys
    main(sys.argv)
