# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import MySQLdb
import time
import requests
from SM_Core.config import config
import re
from tests import covetrics
import urllib2
import os

BaseUrl = "http://artdyachkov.fvds.ru:8080/"

class ParrentHandler(tornado.web.RequestHandler):
    db_instance = None

    def get_connection(self):
        if self.db_instance is None:
            self.db_instance = MySQLdb.connect(
                host=config.dbhost, user=config.dbuser, passwd=config.dbpasswd, db=config.db, charset='utf8',
                port=config.dbport,
            )
        return self.db_instance

    def get_students(self):
        db = self.get_connection()
        cur = db.cursor()
        cur.execute("SELECT s.surname, s.name, s.sex, s.birthday, s.nationality, s.address, s.mark, g.nomer, s.id "
                    "FROM STUDENT s, GROUP_ST g "
                    "WHERE g.id  = s.group_id "
                    "ORDER BY SURNAME")
        students = cur.fetchall()
        return students

    def get_edit_student(self, id_stud):
        db = self.get_connection()
        cur = db.cursor()
        cur.execute(" SELECT s.surname, s.name, s.sex, s.birthday, s.nationality, s.address, s.mark, s.GROUP_ID, s.id "
                    "FROM STUDENT s, GROUP_ST g "
                    "WHERE g.ID  = s.group_id AND s.id = %s " % id_stud)
        student = cur.fetchall()
        return student

    def edit_student(self, surname,  name, sex, birthday, nationality, address, group, id_stud):
        db = self.get_connection()
        cur = db.cursor()
        cur.execute(" UPDATE STUDENT SET surname= %s, name= %s, sex= %s, birthday= %s, nationality= %s, address= %s, group_id= %s "
                    "WHERE ID=%s ",
                    (surname, name, sex, birthday, nationality, address, group, id_stud))

    def add_student(self, surname, name, sex, birthday, nationality, address, mark, group):
        db = self.get_connection()
        cur = db.cursor()
        cur.execute(" INSERT INTO STUDENT (ID, surname, name, sex, birthday, nationality, address, mark, group_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ",
                    (self.id_to_insert(), surname,  name, sex, birthday, nationality, address, mark, group))
        db.commit()

    def id_to_insert(self):
        db = self.get_connection()
        cur = db.cursor()
        cur.execute("SELECT MAX(ID) FROM STUDENT")
        maxid = cur.fetchall()
        idi = int(maxid[0][0]) + 1
        return idi

    def del_student(self, id_stud):
        try:
            db = self.get_connection()
            cur = db.cursor()
            cur.execute("DELETE FROM student WHERE id = %s" % id_stud)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def check_mark(mark):
        if mark == '': return False
        elif re.match(u"^\d(\.\d{1,2})?$", mark) is None: return False
        elif float(mark) < 2 or float(mark) > 5: return False
        else: return True


    @staticmethod
    def check_name(name):
        return re.search(u"^[a-zA-ZА-Яа-я0-9 .\-]{2,30}$", name) is not None

    @staticmethod
    def check_surname(surname):
        return re.search(u"^[a-zA-ZА-Яа-я0-9 .\-]{2,50}$", surname) is not None

    @staticmethod
    def check_address(address):
        return re.match(u"^[a-zA-ZА-Яа-я0-9 ;,.\-]{1,50}$", address) is not None

    @staticmethod
    def check_nationality(nationality):
        return re.match(u"^[a-zA-ZА-Яа-я0-9 .\-]{2,20}$", nationality) is not None

    @staticmethod
    def check_sex(sex):
        return ((sex == u"M") or (sex == u"F"))

    def check_group(self, group):
        if group == '': return False
        else:
            db = self.get_connection()
            cur = db.cursor()
            cur.execute("SELECT COUNT(ID) FROM GROUP_ST WHERE ID = %s " % group)
            groups = cur.fetchall()
            return int(groups[0][0]) >= 1

    @staticmethod
    def check_bitrhday(birthday):
        if not re.match("^\d{4}\-\d{2}\-\d{2}$", birthday):
            return False
        try:
            rdate = time.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            return False
        curdate = time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        if rdate > curdate:
            return False
        return True


class MainHandler(ParrentHandler):
    def get(self):
        students = self.get_students()
        nostud = False
        if students:
            nostud = True
        self.render("static/main.html", students=students, nostud=nostud)

    def post(self):
        self.write('Functional is not yet implemented')


class AddHandler(ParrentHandler):
    def get(self):
        self.render("static/Add.html")

    def post(self):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        group = self.get_argument("group_id")
        mark = self.get_argument("mark")
        sex = self.get_argument("sex")
        birthday = self.get_argument("birthday")
        address = self.get_argument("address")
        nationality = self.get_argument("nationality")

        errors = 'ERRORS LIST: '

        if not self.check_name(name):
            errors += 'Error name! '
        if not self.check_surname(surname):
            errors += 'Error surame! '
        if not self.check_group(group):
            errors += 'Error group! '
        if not self.check_mark(mark):
            errors += 'Error mark! '
        if not self.check_sex(sex):
            errors += 'Error sex! '
        if not self.check_bitrhday(birthday):
            errors += 'Error birthday! '
        if not self.check_address(address):
            errors += 'Error address! '
        if not self.check_nationality(nationality):
            errors += 'Error nation! '

        if errors == 'ERRORS LIST: ':
            self.add_student(surname, name, sex, birthday, nationality, address, mark, group)
            self.redirect("/")
        else:
            self.write(errors)


class DelHandler(ParrentHandler):
    def get(self, id_stud):
        self.del_student(id_stud)
        self.redirect("/")

    def post(self):
        self.write('Functional is not yet implemented')


class EdHandler(ParrentHandler):
    def get(self, id_stud):
        self.render("static/Ed.html", stud=self.get_edit_student(id_stud))

    def post(self, id_stud):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        group = self.get_argument("group_id")
        sex = self.get_argument("sex")
        birthday = self.get_argument("birthday")
        address = self.get_argument("address")
        nationality = self.get_argument("nationality")

        errors = 'ERRORS LIST: '

        if not self.check_name(name):
            errors += 'Error name! '
        if not self.check_surname(surname):
            errors += 'Error surame! '
        if not self.check_group(group):
            errors += 'Error group! '
        if not self.check_sex(sex):
            errors += 'Error sex! '
        if not self.check_bitrhday(birthday):
            errors += 'Error birthday! '
        if not self.check_address(address):
            errors += 'Error address! '
        if not self.check_nationality(nationality):
            errors += 'Error nation! '
        if errors == 'ERRORS LIST: ':
            self.edit_student(name, surname,  group, sex, birthday, address, nationality, id_stud)
            self.redirect("/")
        else:
            self.write(errors)


class ShowHandler(ParrentHandler):
    def get(self):
        db = self.get_connection()

        cur = db.cursor()
        cur.execute(db.get_students())

    def post(self):
        self.write('Functional for post requests is not yet implemented')

AppElementList = []

class CovHandler(ParrentHandler):
    def get(self):
        self.render("static/covetrics.html")
        page = covetrics.PageElementFinder()
        page.GetUrlList(BaseUrl, 2)
        page.FindElements()
        AppElementList = page.TotalElementList

    def post(self):
        try:
            file =self.request.files[self.get_argument('filename')][0]
            filename = file['filename']
        except:
            filename = "/Users/artem/Desktop/StudManager/tests/frontTests.py"
        BaseUrl = self.get_argument("BaseUrl")
        BaseUrl = "http://artdyachkov.fvds.ru:8080/"
        tests = covetrics.TestParser()
        tests.ParseTests(filename)
        pageEls = covetrics.PageElementFinder()
        print "ok"
        pageEls.GetUrlList(BaseUrl, 1)
        print pageEls.UrlList[0]
        response = urllib2.Request(pageEls.UrlList[0])
        print response.headers
        pageEls.FindElements()
        print "ok2"
        print pageEls.TotalElementList
        response = requests.get(BaseUrl)

        self.render('static/covrep.html', BaseUrl=tests.TotalElemetList, filename=pageEls.TotalElementList, testinfo=tests.ParsedTestList)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/add/", AddHandler),
    (r"/delete/(\d+)", DelHandler),
    (r"/edit/(\d+)", EdHandler),
    (r"/cov/", CovHandler),
    (r"/cov/covrep", CovHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/static/"}),

    ])

if __name__ == "__main__":
    application.listen(config.bk_port)
    tornado.ioloop.IOLoop.instance().start()