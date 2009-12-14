import simplejson

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
