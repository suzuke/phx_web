#!/usr/bin/env python
#-_- coding: utf-8 -_-
#author: arno
#introduction:
#    cfapi

import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
logger = logging.getLogger('django')

class CfApi(object):
    def __init__(self, url, email, key):
        self.__url = url.rstrip('/')
        self.__email = email
        self.__key = key
        self.__headers = {'X-Auth-Email': self.__email, 'X-Auth-Key': self.__key, 'Content-Type': 'application/json'}

    def GetDnsLists(self, page=1, status='active', match='all', order='name', direction='asc'):
        url = self.__url + '?per_page=50&page=%s&status=%s&match=%s&order=%s&direction=%s' %(page, status, match, order, direction)
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            return ret.json()
        except:
            return {u'result': [], u'success': False}

    def GetZoneId(self, zone):
        url = self.__url + '?name=%s' %(zone)
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            zone_id = ret.json()['result'][0]['id']
            #logger.info(ret.json())
            return {u'zone_id': zone_id}
        except:
            return {u'zone_id': None}

    def GetZoneRecords(self, zone_id):
        url = self.__url + '/%s/' %zone_id + 'dns_records?per_page=100'
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            return ret.json()
        except:
            return {'result': []}

    def GetDnsRecordId(self, zone_id, record_name):
        self.__record_id = ''
        url = self.__url + '/%s/' %zone_id + 'dns_records?per_page=100&name=%s' %record_name
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            #logger.info(ret.json())
            if len(ret.json()['result']) == 0:
                pass
            elif len(ret.json()['result']) == 1:
                self.__record_id = ret.json()['result'][0]['id']
            else:
                self.__record_id = 'id more than one'
        except:
            self.__record_id = 'bad arguments'

        return self.__record_id

    def UpdateDnsRecords(self, zone_id, record_type, record_name, record_content, proxied=False, record_id=''):
        datas = {'type':record_type, 'name': record_name, 'content': record_content, 'proxied':proxied}
        if record_id == '':
            record_id = self.GetDnsRecordId(zone_id, record_name)
        logger.info('record_id: %s' %record_id)

        if record_id == '':
            return {'result': 'id null'}
        elif record_id == 'id more than one':
            return {'result': 'id more than one'}
        elif record_id == 'bad arguments':
            return {'result': 'bad arguments'}
        else:
            url = self.__url + '/%s/' %zone_id + 'dns_records/'+ record_id
            try:
                logger.info("%s: %s" %(url, datas))
                ret = requests.put(url ,data=json.dumps(datas), headers=self.__headers, verify=False)
                return ret.json()
                logger.info(ret.json())
            except:
                return {'result': {}, 'success': False}

if __name__ == '__main__':
    print 'no'