# -*- coding: utf-8 -*

import re
import urllib

from main_modules.settings import PRIORITY, TYPE
__classificationtype__=TYPE.BackEND_SPECIFIED
__priority__ = PRIORITY.NORMAL


def tamper(payload, **kwargs):
    """
    >>> 
    %55nion(%53elect) <- U=%55 S=%53
%55nion %53eLEct
    """
    
    string=re.sub(r"\w*",convert_this,payload)

    return (string) if payload else payload

def convert_this(string):
    
    string=string.group()
    if len(string)>0:
        string=str(encode(string[:1]))+string[1:]
    return string

def encode(string):
    strt = ""
    con = "%%%02x"
    s = re.compile(r"/|;|=|:|&|@|\\|\?")	
    for c in string:
        if s.search(c):
            strt += c
            continue
        strt += con % ord(c)
    return strt