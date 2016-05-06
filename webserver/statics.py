import os
import re

import falcon

# super quick and dirty static file server

file_cache = {}
ref_path = os.getcwd() + '/static_files'
do_caching = False

def name2type(name):
    rv = 'application/octet-stream'
    if (re.search(r'\.jpg$', name, re.IGNORECASE)):
        rv = 'image/jpeg'
    elif (re.search(r'\.html?$', name, re.IGNORECASE)):
        rv = 'text/html'
    elif (re.search(r'\.css$', name, re.IGNORECASE)):
        rv = 'text/css'
    elif (re.search(r'\.txt$', name, re.IGNORECASE)):
        rv = 'text/plain'
    elif (re.search(r'\.js$', name, re.IGNORECASE)):
        rv = 'application/javascript'

    return rv

class StaticStuff(object):
    def on_get(self, req, resp, fname):
        fpath = '/'.join((ref_path,fname))
        print(fpath)
        if do_caching and fname in file_cache:
            print('Getting from cache.')
            resp.data = file_cache[fname]['content']
            resp.status = falcon.HTTP_200
            resp.content_type = file_cache[fname]['type']
            return
        elif os.path.isfile(fpath):
            with open(fpath,'rb') as content_file:
                content = content_file.read()
                file_cache[fname] = {
                    'content': content,
                    'type': name2type(fname)
                }
            print('Getting from disk.')
            resp.data = file_cache[fname]['content']
            resp.status = falcon.HTTP_200
            resp.content_type = file_cache[fname]['type']

        else:
            resp.body = 'Not found.'
            resp.status = '404 Not Found'


            



