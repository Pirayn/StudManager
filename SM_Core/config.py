import os



class GenericConfig(object):
    def __init__(self):
        self.dbuser = 'root'
        self.dbpasswd = 'aswedro'
        self.db = 'STUDENTS'
        self.dbhost = '127.0.0.1'
        self.dbport = 3306
        self.host = '127.0.0.1'
        self.bk_port = 8080


config = GenericConfig()

