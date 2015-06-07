# -*- coding: utf-8 -*-
from server import ParrentHandler
import pytest
import tornado.ioloop
import tornado.web
import MySQLdb
import time
from SM_Core.config import config
import re
import urllib
from tornado.options import define, options
from tornado.httpclient import HTTPClient, HTTPError
import os
from torndb import Connection
import httplib
import datetime


def get_studs_count(ConnectToDB):
    qrez = ConnectToDB.get(" SELECT COUNT(*) as c  FROM STUDENT; ")
    print(int(qrez['c']))
    return int(qrez['c'])


def empty_studs(ConnectToDB):
    ConnectToDB.execute(" DELETE FROM STUDENT ")


def empty_groups(ConnectToDB):
    ConnectToDB.get(" DELETE FROM GROUP_ST ")


def exec_dump():
    os.system("mysql -uroot  < dump.sql")


def add_group(ConnectToDB):
    ConnectToDB.execute(" INSERT INTO GROUP_ST (ID, NOMER, SUB_FAC_ID) VALUES (100, 'Б8-01' ,100) ")


def add_stud(ConnectToDB):
    ConnectToDB.execute(" INSERT INTO STUDENT (ID, SURNAME, NAME, SEX, BIRTHDAY, NATIONALITY, ADDRESS, MARK, GROUP_ID ) "
                         "VALUES ('12345', 'ИВАНОВ', 'ТАБУРЕТЧИК', 'M', '1989-10-11', 'рус', 'Волочаевская д.5 кв. 38', '3.12', '100') ")


@pytest.fixture(scope='function')
def ConnectToDB(request):
    DBConnection = Connection(host='127.0.0.1', database='STUDENTS', user='root')

    def fin():
        print ("Teardown DBConnection")
        DBConnection.close()

    request.addfinalizer(fin)
    return DBConnection


@pytest.fixture(scope='function')
def ConnectToServer(request):
    ServerConnection = httplib.HTTPConnection("localhost:8080")

    def fin():
        print ("Teardown ServerConnection")
        ServerConnection.close()

    request.addfinalizer(fin)
    return ServerConnection


@pytest.fixture(scope='function')
def empty_db(ConnectToDB):
    empty_studs(ConnectToDB)
    empty_groups(ConnectToDB)


@pytest.fixture(scope='function')
def DBDefault():
    exec_dump()


@pytest.mark.usefixtures('DBDefault')
def test_1_MainPage_Full(ConnectToServer, ConnectToDB):
    ConnectToServer.request('GET', '/')
    resp = ConnectToServer.getresponse()
    telo = resp.read()
    x = len(re.findall("delete", telo))
    assert resp.status == 200
    assert 'No students yet' not in telo
    assert get_studs_count(ConnectToDB) == x


@pytest.mark.usefixtures('ConnectToServer', 'empty_db')
def test_2_MainPage_Empty(ConnectToServer):
    ConnectToServer.request('GET', '/')
    resp = ConnectToServer.getresponse()
    telo = str(resp.read())
    assert resp.status == 200
    assert 'No students yet' in telo


@pytest.mark.usefixtures('ConnectToServer')
def test_3_MainPage_Post(ConnectToServer):
    ConnectToServer.request('POST', '/')
    resp = ConnectToServer.getresponse()
    assert resp.status == 404


@pytest.mark.usefixtures('ConnectToServer')
def test_4_AddPage_Show(ConnectToServer):
    ConnectToServer.request('GET', '/add')
    resp = ConnectToServer.getresponse()
    telo = resp.read()
    assert resp.status == 200
    assert 'form action="add" method="post' in telo
    assert 'name' in telo
    assert 'surname' in telo
    assert 'sex' in telo
    assert 'birthday' in telo
    assert 'nationality' in telo
    assert 'address' in telo
    assert 'group_id' in telo
    assert 'mark' in telo


@pytest.mark.usefixtures('ConnectToServer', 'DBDefault', 'ConnectToDB')
@pytest.mark.parametrize('param, value', [
        ('name', 'Вованчик'),
        ('name', 'Вoванчик Красный'),
        ('name', 'Вован-чик'),
        ('name', 'Вован.чик'),
        ('name', 'Vovanchik.'),
        ('name', 'Во'),
        ('name', 'И2в'),
        ('name', 'В'*30),
        ('surname', 'Беулов'),
        ('surname', 'Belov'),
        ('surname', 'Бел0в'),
        ('surname', 'Белов Белов'),
        ('surname', 'Бел.ов'),
        ('surname', 'Б-елов'),
        ('surname', 'Бе'),
        ('surname', 'б'*50),
        ('sex', 'M'),
        ('sex', 'F'),
        ('birthday', '1889-11-11'),
        ('birthday', '2000-01-01'),
        ('birthday', str(datetime.date.today())),
        ('nationality', 'Русский'),
        ('nationality', 'Italian'),
        ('nationality', 'U.K'),
        ('nationality', 'афро американец'),
        ('nationality', 'русс-к'),
        ('nationality', 'рус1'),
        ('nationality', 'RU'),
        ('nationality', 'X'*20),
        ('address', 'Посёлок'),
        ('address', 'SPB'),
        ('address', 'Москва1'),
        ('address', 'г Москва'),
        ('address', 'н. Москва'),
        ('address', 'пр-д'),
        ('address', 'д5,кв47'),
        ('address', 'Жопамира;'),
        ('address', 'м'),
        ('address', 'м'*50),
        ('group_id', '100'),
        ('mark', '3.45'),
        ('mark', '3.4'),
        ('mark', '4'),
        ('mark', '2.00'),
        ('mark', '5.00'),
    ])
def test_5_AddStudent_P(param, value, ConnectToServer, ConnectToDB):
        #empty_studs(ConnectToDB)
        cases = {'name': 'Вован', 'surname': 'Белов', 'group_id': '100',  'mark': '3.23', 'sex': 'M', 'birthday': '2000-11-09',
                 'address': 'урюпинск 321', 'nationality': 'рус'}
        cases[param] = value
        body = urllib.urlencode(cases)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        ConnectToServer.request('POST', '/add', body=body, headers=headers)
        resp = ConnectToServer.getresponse()
        assert resp.status == 302
        assert get_studs_count(ConnectToDB) == 32
        #assert check_student_add(database, cases)


@pytest.mark.usefixtures('ConnectToServer', 'DBDefault', 'ConnectToDB')
@pytest.mark.parametrize('param, value', [
        ('name', '/7awok'),
        ('name', 'G'),
        ('name', 'G'*31),
        ('name', ''),
        ('surname', 'asd*'),
        ('surname', 'd'),
        ('surname', 'd'*51),
        ('surname', ''),
        ('sex', 'D'),
        ('sex', ''),
        ('sex', 'мужик'),
        ('birthday', '12-12-1992'),
        ('birthday', '1990-02-45'),
        ('birthday', '1990-02-29'),
        ('birthday', '2150-01-22'),
        ('birthday', ''),
        ('nation', 'рус %'),
        ('nation', 'Й'),
        ('nation', 'Й'*21),
        ('nation', ''),
        ('address', '+Москоу+'),
        ('address', 'в'*51),
        ('address', ''),
        ('group_id', 'ййй'),
        ('group_id', '2731'),
        ('group_id', ''),
        ('mark', '2.123'),
        ('mark', '3.'),
        ('mark', '1.99'),
        ('mark', '5.01'),
        ('mark', '-3.44'),
        ('mark', ''),
    ])
def test_6_AddStudent_N(param, value, ConnectToServer, ConnectToDB):
    #empty_studs(ConnectToDB)
    cases = {'name': 'Вован', 'surname': 'Белов', 'group_id': '100',  'mark': '3.23', 'sex': 'M', 'birthday': '2000-11-09',
             'address': 'урюпинск 321', 'nationality': 'рус'}
    cases[param] = value
    body = urllib.urlencode(cases)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    ConnectToServer.request('POST', '/add', body=body, headers=headers)
    resp = ConnectToServer.getresponse()
    assert resp.status == 200
    assert get_studs_count(ConnectToDB) == 31
    assert 'Error '+param in resp.read()


@pytest.mark.usefixtures('ConnectToServer', 'ConnectToDB')
def test_6_DelPage_Show():
    add_stud(ConnectToDB)
    ConnectToServer.request('GET', '/delete/12345')
    resp = ConnectToServer.getresponce()
    telo = resp.read()
    assert resp.status == 200
    assert 'ТАБУРЕТЧИК ИВАНОВ, 1989-10-11' in telo


@pytest.mark.usefixtures('empty_db', 'ConnectToServer')
def test_7_DelPage_N():
    add_stud(ConnectToDB)
    ConnectToServer.request('GET', '/delete/12341231325')
    resp = ConnectToServer.getresponce()
    assert resp.status == 404


@pytest.mark.usefixtures('empty_db', 'ConnectToServer', 'ConnectToDB')
def test_8_DelStud_YES_P():
    add_stud(ConnectToDB)
    body = {'answer': 'yes'}
    body = urllib.urlencode(body)
    ConnectToServer.request('POST', '/delete/12345', body=body, headers=None)
    resp = ConnectToServer.getresponce()
    assert resp.status == 302
    assert get_studs_count(ConnectToDB) == 0


@pytest.mark.usefixtures('empty_db', 'ConnectToServer', 'ConnectToDB')
def test_9_DelStud_YES_N():
    body = {'answer': 'yes'}
    body = urllib.urlencode(body)
    ConnectToServer.request('POST', '/delete/123457777', body=body, headers=None)
    resp = ConnectToServer.getresponce()
    assert resp.status == 404


@pytest.mark.usefixtures('empty_db', 'ConnectToServer', 'ConnectToDB')
def test_10_DelStud_NO():
    add_stud(ConnectToDB)
    body = {'answer': 'no'}
    body = urllib.urlencode(body)
    ConnectToServer.request('POST', '/delete/12345', body=body, headers=None)
    resp = ConnectToServer.getresponce()
    assert resp.status == 302
    assert get_studs_count(ConnectToDB) == 1






















