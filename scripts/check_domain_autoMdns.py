#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#introduciton:
#    域名故障，自动切换线路，并实时预警
#version: 2018/12/26  实现基本功能

import os, sys, datetime, logging, multiprocessing, requests, json, urlparse, threading, platform, commands

#reload(sys)
#sys.setdefaultencoding('utf8')

#将上层目录加入环境变量，用于引用其他模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

#设置django环境
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'phxweb.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
django.setup() #启动django

from detect.telegram import sendTelegram
from monitor.models  import project_t, minion_t, minion_ip_t
from detect.models   import domains
from phxweb          import settings

from bs4        import BeautifulSoup
from time       import sleep
#from color_print import ColorP
from socket     import gethostname, gethostbyname
#from subprocess import getoutput

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#telegram 参数
message = settings.message_TEST

#状态定义
error_status  = u'失败'
normal_status = [200, 404, 403]

#当前脚本路径
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

#获取html的title
def getHtmlTitle(html):
    html = BeautifulSoup(html,'html.parser')
    try:
        return html.title.text
    except:
        return None

def getDomains():
    '''
        获取需要监控的域名列表
    '''
    domain_list  = []
    projects = project_t.objects.filter(autoMdns=1).all() #获取所有项目
    for project in projects:
        tmp_dict = {

        }

    return domain_list

class ReqIps(object):
    '''
        执行检测ip
    '''
    def __init__(self, arg):
        '''
            初始化检测参数
        '''
        self.__project  = arg['project']
        self.__url      = arg['url']
        self.__uri      = '/'
        self.__name     = ''
        self.__product  = ''
        self.__customer = ''
        self.__method   = 'head'
        self.__verify   = False
        self.__timeout  = 10
        self.__retry    = 3
        self.__reg      = '^.*[a-zA-Z0-9]+.*\.[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$'
        self.__headers  = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        domain = arg['domain']
        if isinstance(domain, dict):
            if ('client' in domain.keys()) and domain['client'] == 'wap': self.__headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
            if 'method' in domain.keys(): self.__method = domain['method']
            #if ('ssl' in domain.keys()) and domain['ssl'] != 1: self.__verify = False
            if 'timeout' in domain.keys(): self.__timeout = domain['timeout']
            if 'product' in domain.keys(): self.__product = domain['product'][1]
            if 'customer' in domain.keys(): self.__customer = domain['customer'][1]
            if 'name' in domain.keys() and len(domain['name'].split('/')) >= 3: 
                self.__name = urlparse.urlsplit(domain['name']).netloc.split(':')[0].strip()
                self.__headers['Host'] = self.__name
                self.__uri  = urlparse.urlsplit(domain['name']).path
    def ExeReq(self):
        '''执行域名检测'''
        res = []
        s   = requests.Session()
        url = self.__url.strip() + self.__uri
        req = requests.Request(
                method  = self.__method.strip(), 
                url     = url, 
                headers = self.__headers
            ).prepare()
        try:
            ret = s.send(req, verify=self.__verify, timeout=self.__timeout)
        except requests.exceptions.ConnectTimeout:
            res.append({error_status: {url:u'连接超时！'}})
        except requests.exceptions.ReadTimeout:
            res.append({error_status: {url:u'加载超时！'}})
        except requests.exceptions.SSLError:
            res.append({error_status: {url:u'证书认证错误！'}})
        #except requests.exceptions.NewConnectionError:
        #    res.append({error_status: {url:u'找不到主机名！'}})
        except requests.exceptions.MissingSchema:
            res.append({error_status: {url:u'协议头无效！'}})
        except requests.exceptions.ConnectionError:
            res.append({error_status: {url:u'连接错误！'}})
        except Exception as e:
            res.append({error_status: {url:str(e)}})
        else:
            if len(ret.history) != 0:
                for r in ret.history:
                    res.append({r.status_code: r.url})
            res.append({ret.status_code: ret.url})
            res.append({'title': getHtmlTitle(ret.content)})
        return res

class myThread(threading.Thread):
    def __init__(self, arg):
        threading.Thread.__init__(self)
        self.arg = arg

    def run(self):
        rd = ReqIps(self.arg)
        self.__product  = rd.__dict__['_ReqIps__product']
        self.__customer = rd.__dict__['_ReqIps__customer']
        self.t          = None

        for i in range(rd.__dict__['_ReqIps__retry']):
            res = rd.ExeReq()
            print self.__product + "_" +self.__customer, rd.__dict__['_ReqIps__name'], str(res).decode("unicode-escape")

            if error_status not in res[0].keys() and res[-2].keys()[0] in normal_status:
                break
            sleep(2)
        if error_status in res[0].keys():
            self.t = ": ".join([self.__product, rd.__dict__['_ReqIps__name'], str(res[0][error_status]).decode("unicode-escape")])
        elif res[-2].keys()[0] not in normal_status:
            self.t = ": ".join([self.__product, rd.__dict__['_ReqIps__name'], str(res).decode("unicode-escape")])

    def get_result(self):
        if self.t:
            return [self.arg['domain']['product'][0], self.t] 
        else:
            return None

def getIp():
    try:
        ret = requests.get('http://myip.ipip.net')
    except Exception as e:
        print u'获取当前IP失败......'
        print str(e)
        ip = gethostname()
    else:
        if ret.status_code == 200:
            ip = ret.text
        else:
            ip = gethostname()
    return ip

def sendAlert(ip, results):
    java      = ""
    ruiying   = ""
    fenghuang = ""
    for result in results:
        if result[0] == 26:
            java += '\r\n' + result[1]
        elif result[0] == 27:
            ruiying += '\r\n' + result[1]
        else:
            fenghuang += '\r\n' + result[1]
    if java:
        message['doc']  = False
        message['text'] = ip + java
        message['group'] = 'java_domain' #java_domain
        if len(message['text']) >= 4096:
            message['doc']  = True
            message['text'] = message['text'].replace('\r\n', '\n')
        sendTelegram(message).send()
    if ruiying:
        message['doc']  = False
        message['text'] = ip + ruiying
        message['group'] = 'arno_test' #ruiying_domain
        if len(message['text']) >= 4096:
            message['doc']  = True
            message['text'] = message['text'].replace('\r\n', '\n')
        sendTelegram(message).send()
    if fenghuang:
        message['doc']  = False
        message['text'] = ip + fenghuang
        message['group'] = 'domain_alert' #domain_alert
        if len(message['text']) >= 4096:
            message['doc']  = True
            message['text'] = message['text'].replace('\r\n', '\n')
        sendTelegram(message).send()

if __name__ == '__main__':
    if platform.system() == "Linux":
        ip = commands.getoutput('curl -s https://ip.cn')
    else:
        ip = getIp()

    print ip
    print getDomains()

    sys.exit()

    li = []
    results = []

    for arg in getIps('nginx'):
        t = myThread(arg)
        li.append(t)
        t.start()
    for t in li:
        t.join()
        if t.get_result(): results.append(t.get_result())

    sendAlert(ip, results)