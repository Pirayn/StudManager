# -*- coding: utf-8 -*-
import json
import httplib
import urllib
import re
import xml.etree.ElementTree as etree
import time


def GetFragment(Name, BitRate, url, UrlTemplate, Fragment):
    """Функция загруки фрагмента"""
    """Склеиваем урл фрагмента"""
    FragtUrl = url[0:url.rfind('/')] + '/' + UrlTemplate.format(bitrate=BitRate, starttime=Fragment.values()[0])
    print Name, BitRate, Fragment.keys()[0], ": ", FragtUrl

    """Загрузка фрагмента вместе с замером времени"""""
    start = time.time()
    f1 = urllib.urlopen(FragtUrl)
    finish = time.time()
    
    if f1.code == 200:
        print 'CODE:', f1.code, '     TIME:', finish-start, '     Response Length:', f1.info().get('content-length')
    else:
        print 'FAILED! Because code is', f1.code


def testget():
    """Подключаемся к хосту и получаем список доступных ресурсов"""
    ConnectToServer = httplib.HTTPConnection("test1.play.mc.dc.nemotele.com")
    ConnectToServer.request('GET', '/api/v1/resources/')

    """Запихиваем в список не более 3х ресурсов из предыдущего ответа"""
    resource_list = re.split(',', re.sub('\[|\]|\"| ', '', ConnectToServer.getresponse().read()))[0:3]
    delivery_list = [30, 31, 32]

    """2 цикла, в которых будут перебираться все варианты связки Resource-id + Delivery-id,
        для подставноки в ПОСТ запрос на получение ссылки"""
    for rid in resource_list:
        for did in delivery_list:
            body = {
                    "protocol": "smooth",
                    "resource_id": rid,
                    "delivery_id": did,
                    "device_type": "default",
                    "drm": "plain",
                    "ip": "*",
                    "lifetime": 600,
                    "maxstreams": 0,
                    "stream_pool_id": 0,
                    "user_id": "test_user",
                    }
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            ConnectToServer.request('POST', '/api/v1/generate_url_extended', body=urllib.urlencode(body), headers=headers)

            """Подготовка и выстрел по сгенерившейся ссылки для получения манифеста"""
            url = json.loads(ConnectToServer.getresponse().read())['streaming_url']
            manifest = urllib.urlopen(url)

            print
            print
            print '-'*100
            print 'Resource:', rid, '| Delivery:', did
            print url
            print 'Manifest response status:', manifest.code
            print 'Tracks fragments:'

            """Парсинг тела ответа"""
            tree = etree.ElementTree(etree.fromstring(manifest.read()))
            root = tree.getroot()

            i=0
            """Цикл, в котором мы идем по всем трекам в манифесте и выдергиваем фрагменты"""
            while i < len(root):
                """Проверяем, являеется ли элемент треком"""""
                if root[i].tag == 'StreamIndex':
                    "Сделаем список из доступных битрейтов"
                    QualityLevelList = root[i].findall('QualityLevel')
                    BitRateList = []
                    for QaulityLevel in QualityLevelList: BitRateList.append(QaulityLevel.get('Bitrate'))

                    """Подготовка переменных"""
                    Name = root[i].attrib.get('Name')
                    UrlTemplate = re.sub(' ', '', root[i].attrib.get('Url'))
                    AllFragList = (root[i].findall('c'))
                    """Фрагменты в видже джейсона, так удобнее пихать в функцию и делать более информативный вывод"""
                    FragFirst = {'First': AllFragList[0].attrib.get('t')}
                    FragMid = {'Mid': AllFragList[int(len(AllFragList)/2)].attrib.get('t')}
                    FragLast = {'Last': AllFragList[-1].attrib.get('t')}

                    """Перебираем все битрейты и дергаем функцию загрузки соотв. фрагмента"""
                    for BitRate in BitRateList:
                        GetFragment(Name, BitRate, url, UrlTemplate, FragFirst)
                        GetFragment(Name, BitRate, url, UrlTemplate, FragMid)
                        GetFragment(Name, BitRate, url, UrlTemplate, FragLast)
                        print

                    i += 1
                else:
                    i += 1


testget()

