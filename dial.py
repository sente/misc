#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import os, sys
from re import sub
import time
import pprint

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

print "content-type: text/html\n\n"

vars={
    "username":"",
    "password":"",

    "tainted_username":"",
    "tainted_password":"",

    "address":"",
    "agent":"",
    "timestr":"",
    "referer":"",

    "status":"okay",
    "message":"",
}


def do_input(vars):
    form = cgi.FieldStorage()

    vars["tainted_username"] = form.getfirst("username", "")
    vars["tainted_password"] = form.getfirst("password", "")

    vars["agent"]=os.environ.get("HTTP_USER_AGENT")
    vars["address"]=os.environ.get("REMOTE_ADDR")
    vars["referer"]=os.environ.get("HTTP_REFERER")

    if vars["referer"] == None: vars["referer"]=""
    if vars["agent"] == None: vars["agent"]=""
    if vars["address"] == None: vars["address"]=""


def do_sanitize(vars):

    vars["username"] = sub(r'[^a-zA-Z0-9_]','',vars["tainted_username"])
    vars["password"] = sub(r'[^a-zA-Z0-9_]','',vars["tainted_password"])

    if vars["tainted_username"]!=vars["username"] or vars["tainted_password"]!=vars["password"]:
        vars["message"] = "The username and password can only contain the characters: [a-zA-Z0-9_]"
        vars["status"]="fail"
        return -1

    for s in [vars["username"],vars["password"]]:
        if len(s) < 4 or len(s) > 20:
            vars["message"] = "The username and password must be between 4 and 20 characters"
            vars["status"]="fail"
            return -1

    return 0


def do_logit(vars):
    logfile= "/usr/lib/cgi-bin/dial/logs/logs.txt"

    r=[]
    r.append(time.strftime("%F %H:%m:%S"))
    r.append(vars["status"])
    r.append(vars["address"])
    r.append(vars["username"])
    r.append(vars["password"])


    foo=open(logfile,"a")
    foo.write("\t".join(r))
    foo.write("\n")
    foo.close()


def do_output(vars):

    print "<html><body><pre>"

    if vars["status"] == "fail" :
        print "Hmm...it seems something went wrong...<br/>%s" % vars["message"]
        print "please go back and try again: ",
        print "<a href=\"http://www.sente.cc/dial.html\">http://www.sente.cc/dial.html<a/>"
    else:
        print "cgi success!"
        print "now to plug the data into di-controller..."

    print "<br/><br/><br/>"
    print "<br/><br/><br/>"

    print "username: " +  vars["username"]
    print "password: " +  vars["password"]

    print "address:" + vars["address"]
    print "referer:" + vars["referer"]
    print "agent:" + vars["agent"]

    print "</pre></body></html>"


do_input(vars)

flag=do_sanitize(vars)

do_logit(vars)

do_output(vars)
