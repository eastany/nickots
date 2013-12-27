#-*- coding:utf-8 -*-
#!/usr/bin/env python

import urllib2,os,cookielib,urllib

class RenRenRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301( self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        result.status = code
        return result

def get_url(opener,url,fname=None):
    req = urllib2.Request(url)
    
    res = opener.open(req).read()
    if fname:
        f=open(fname,'w+')
        f.write(res)
        f.close()
    return res

def post_url(opener,url,data):
    req = urllib2.Request(url,urllib.urlencode(data))
    return opener.open(req).read()
