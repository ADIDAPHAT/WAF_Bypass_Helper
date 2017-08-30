# -*- coding: utf-8 -*

import urlparse
import requests
import urllib
import re
from difflib import Differ
import sys


from settings import NETWORK


def get_sender(url,bypass=None,cookie=None,useproxy=None,get_full_request=False,request_param_for_atack=None,post=None,injfile=None):
    request_param_for_atack=str(request_param_for_atack)
    cookie_inject_name=None
    if injfile:
        our_request=get_request_from_file(injfile)
        host=our_request.get('Host')
        Body=our_request.get('Body')
        url_path=our_request.get('url_path')
        url=host+url_path
      
        request_type=our_request.get('request_type')
        if request_type=='POST':
            post=Body
        headers=our_request
        my_pop(headers,'Body')
        my_pop(headers,'url_path')
        my_pop(headers,'Content-Lengt')
        my_pop(headers,'request_type')
       

        url='http://'+url
        SplitResult=urlparse.urlsplit(url)
    else:
        SplitResult=urlparse.urlsplit(url)
        host=SplitResult.netloc
        user_agent=NETWORK.user_agent
        accept_language=NETWORK.accept_language
        content_type= NETWORK.content_type
        accept_encoding=NETWORK.accept_encoding
        referer=url
        headers={'Host':host,'User-Agent':user_agent,'Content-Type':content_type,'Accept-Language':accept_language,'Accept-Encoding':accept_encoding,'Referer':referer} 

    if re.search('cookie:',request_param_for_atack):
        #inject in cookie
        cookie_inject_name=request_param_for_atack.split(':')[1]
    if type(request_param_for_atack)==str:
        request_param_for_atack=re.split('[|;,]',request_param_for_atack)
    if post:
        meanings_array=[]
        param_array=[]
        for el in post.split('&'):
            param_array.append((re.search(r'\S*(?=\=)',el)).group())
            meanings_array.append((re.search(r'(?<==)\S*',el)).group())
        
    else:
        param_array=re.findall(r'(?<=^)\S*?(?=\=)',SplitResult.query)
        param_array=param_array+(re.findall(r'(?<=&)\S*?(?=\=)',SplitResult.query))
        if len(request_param_for_atack)==0 and len(param_array)>1:
            print("I dont know param for inject. Pls use -p name_of_param")
        if re.findall(r'&',SplitResult.query) is not None:
            meanings_array=re.findall(r'(?<==)\S*?(?=&)',SplitResult.query)
            last_param=re.escape(param_array[-1])
            meanings_array=meanings_array+re.findall(r'(?<='+last_param+'=)\S*?(?=$)',SplitResult.query)
        else:
            meanings_array=re.findall(r'(?<=\=)\w*',SplitResult.query)
    if bypass:       
        bypass=urllib.quote_plus(bypass, safe='/%')
        if post:
            my_url=''
        else:
            my_url=SplitResult.scheme+'://'+SplitResult.hostname+'/'+SplitResult.path+'?'
        postdata=''
        i=0
        for param in param_array:
            
            for prm_to_atack in request_param_for_atack:
                if param==prm_to_atack:
                    meanings_array[i]=bypass
            i+=1
        i=0
        for param in param_array:   
            my_url=my_url+'&'+str(param)+'='+str(meanings_array[i])
            postdata=postdata+'&'+str(param)+'='+str(meanings_array[i])
            i+=1
        if post:
            postdata=postdata[1:]
            my_url=my_url[1:]
            my_url=url+my_url

    http_proxy  = NETWORK.http_proxy
    https_proxy = NETWORK.https_proxy
    proxyDict = { 
                "http"  : http_proxy, 
                "https" : https_proxy,
            }
    cookie_param_array=[]
    cookie_meanings_array=[]
    inj_cookie={}
    if cookie:
        cookies=cookie.split(';')
        for cookie_el in cookies:
            cookie_param_array.append((re.search(r'\S*(?=\=)',cookie_el)).group())
            cookie_meanings_array.append((re.search(r'(?<==)\S*',cookie_el)).group())
            if cookie_inject_name and cookie_inject_name==cookie_param_array[-1]:
                cookie_meanings_array[-1]=bypass
            inj_cookie.update({cookie_param_array[-1]:cookie_meanings_array[-1]})

    if useproxy:
        try:
            if post:
                response=requests.post(url,cookies=inj_cookie,proxies=proxyDict,data=postdata,headers=headers)
            else: 
                response=requests.get(my_url,cookies=inj_cookie,proxies=proxyDict,headers=headers)
        except requests.exceptions.InvalidHeader:
            print ("Error Headers")
            print headers
            sys.exit()
        except requests.exceptions.ConnectionError:
            print("Can not connect to "+url)
            print("We use proxy:"+http_proxy)
            sys.exit()
        except :
            print("Strange problem this request "+url+" Error:"+str(sys.exc_info()[0]))
            print("We use proxy:"+http_proxy)
            sys.exit()
    else:
        try:
            if post:
                response=requests.post(url,data=postdata,cookies=inj_cookie,headers=headers)            
            else:
                response=requests.get(my_url,cookies=inj_cookie,headers=headers)
        except requests.exceptions.InvalidHeader:
            print ("Error Headers")
            print headers
            sys.exit()                
        except requests.exceptions.ConnectionError:
            print("Can not connect to "+url)
            sys.exit()
        except :
            print("Strange problem this request "+url+" Error:"+str(sys.exc_info()[0]))
            sys.exit()

    if (get_full_request==True):
        return(response.content)
    return(response.status_code)

def my_pop(mdict,name):
    try:
        mdict.pop(name)
    except:
        pass
    return mdict

def response_dif(response1,response2):
    d=Differ()
    diff = d.compare(response1, response2)
    i=0
    for el in diff:
        if re.match(r'\+|-',el):
            i+=1
    return i

def get_request_from_file(file):
    request_file=open(file,'r')
    request={}
    i=0
    body=0
    for line in request_file:
        line=re.sub(r'\r','',line)
        if i==0:

            type_of_request=re.search(r'\w+(?=\s)?',line).group()
            url_path=re.search(r'(?<=\s)/\S*',line).group()
            http_type=re.search(r'HTTP.*',line).group()
            request.update({'request_type':type_of_request,'url_path':url_path,'http_type':http_type})
            i+=1
            continue
        if re.search(r':',line):
            name=re.search(r'\S+(?=:)',line).group()
            meaning=re.search(r'(?<=:).*',line).group().lstrip()
            request.update({name:meaning})
        elif re.search(r'\w',line) is None:
            i+=1
            body=1
            continue
        elif body==1:
            if request.get('Body'):
                request.update({'Body':request.get('Body')+line})
            else:
                request.update({'Body':line})
        i+=1
    request_file.close()
    return request

def bypass_tester(my_url,bypass,cookie,proxy,response,request_param_for_atack,post,injfile):
    result=get_sender(my_url,bypass,cookie,proxy,response,request_param_for_atack,post,injfile)
    if response==False:
        if str(result)[0]=='4':

            return 0
        elif  str(result)[0]=='5':

            return 2
        elif  str(result)[0]=='2':

            return 1
        elif  str(result)[0]=='3':
 
            return 1
        else:
            print ('Nothing '+str(result)[0])
            return 0


