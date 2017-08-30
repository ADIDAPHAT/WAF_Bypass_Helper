# -*- coding: utf-8 -*
import re
from main_modules.settings import PRIORITY, TYPE
__classificationtype__=TYPE.BackEND_SPECIFIED
__priority__ = PRIORITY.NORMAL




def tamper(payload, **kwargs):
    """
    >>> tamper("<iframe src=http://ha.ckers.org/scriptlet.html>")
<iframe src=http://ha.ckers.org/scriptlet.html <
    """

    return re.sub(r">(?!\S)","<",payload,1) if payload else payload
    

