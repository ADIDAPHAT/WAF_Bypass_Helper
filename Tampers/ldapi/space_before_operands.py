import re

from main_modules.settings import PRIORITY, TYPE
__classificationtype__=TYPE.UNIVERSAL
__priority__ = PRIORITY.NORMAL

def tamper(payload, **kwargs):
    """

   
    """
    result=[]
    result.append(re.sub(r"\|",'%0a',payload))
    result.append(re.sub(r"\|",'%00',payload))
    result.append(re.sub(r"\|",'%20',payload))
    result.append(re.sub(r"\|",'%09',payload))
    result.append(re.sub(r"\|",'%0B',payload))
    result.append(re.sub(r"\|",'%0C',payload))



    return result if payload else payload

