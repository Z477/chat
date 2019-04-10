import ast
import json
import datetime

from controller import controller, onRequset
import pymysql.cursors
from urlparse import parse_qs


@controller
class Test1Controller:
    def __init__(self):
        pass

    def to_json(self, sql_result):
        '''
        @summary change select sql_result to json format
        @param sql_result: cursor.fetchall() result
        @return: json format result
        '''

        data_detail = []
        new_result = {}
        f = '%Y-%m-%d %H:%M:%S'
        for row in sql_result:
            row_new = {}
            for key, value in row.items():
                key_new = key.encode("utf-8")
                if type(value) == datetime.datetime:
                    value_new = value.strftime(f)
                elif  type(value) == int:
                    value_new = value
                else:
                    value_new = value.encode("utf-8")
                row_new.update({key_new:value_new})
            new_result.update(row_new)
            data_detail.append(ast.literal_eval(json.dumps(new_result)))
        return data_detail

    @onRequset(url="/user/username", method='GET')
    def getUserName(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'GET'),
                                  ('Access-Control-Allow-Headers', 'x-requested-with,content-type')])
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # get data from mysql
                query_str_dict = parse_qs(environ['QUERY_STRING'])
                id = query_str_dict.get('id', [''])[0]
                reverse = query_str_dict.get('reverse', [''])[0]
                if reverse == 'false':
                    sql_1 = "select * from user where id={};".format(id)
                else:
                    sql_1 = "select * from user where id!={};".format(id)
                cursor.execute(sql_1)
                result = cursor.fetchall()

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        content = json.dumps({"status": 0, "reason": '', "data": result})
        return ['{}'.format(content)]

    @onRequset(url="/user/userlist", method='GET')
    def getUserList(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'GET'),
                                  ('Access-Control-Allow-Headers', 'x-requested-with,content-type')])
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # get data from mysql
                sql_1 = "select * from user;"
                cursor.execute(sql_1)
                result = cursor.fetchall()

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        content = json.dumps({"status": 0, "reason": '', "data": result})
        return ['{}'.format(content)]

    @onRequset(url="/user/records", method='GET')
    def getRecords(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'GET'),
                                  ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')])
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # get data from mysql
                query_str_dict = parse_qs(environ['QUERY_STRING'])
                sender_id = int(query_str_dict.get('sender', [''])[0])
                receiver_id = int(query_str_dict.get('receiver', [''])[0])

                sql_str = "select * from chat_record where ((sender={sender_id} and receiver={receiver_id}) or (sender={receiver_id} and receiver={sender_id})) order by id limit 9;".format(
                        sender_id=sender_id, receiver_id=receiver_id)
                cursor.execute(sql_str)
                result = cursor.fetchall()
                new_result = self.to_json(result)
                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

            content = json.dumps({"status": 0, "reason": '', "data": new_result})

        return ['{}'.format(content)]

    @onRequset(url="/user/history", method='GET')
    def getHistory(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'GET'),
                                  ('Access-Control-Allow-Headers', 'x-requested-with,content-type')])
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # get data from mysql
                query_str_dict = parse_qs(environ['QUERY_STRING'])
                sender_id = int(query_str_dict.get('sender', [''])[0])
                receiver_id = int(query_str_dict.get('receiver', [''])[0])
                beforechat_id = int(query_str_dict.get('beforechatid', [''])[0])

                sql_str = "select * from chat_record where id<{beforechat_id} and ((sender={sender_id} and receiver={receiver_id}) or (sender={sender_id} and receiver={receiver_id})) order by id limit 9;".format(
                        beforechat_id=beforechat_id)
                cursor.execute(sql_str)
                result = cursor.fetchall()

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        content = {"status": 0, "reason": '', "data": result}
        return ['{}'.format(content)]

    @onRequset(url="/user/newrecords", method='GET')
    def getNewRecord(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'GET'),
                                  ('Access-Control-Allow-Headers', 'x-requested-with,content-type')])
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # get data from mysql
                query_str_dict = parse_qs(environ['QUERY_STRING'])
                sender_id = int(query_str_dict.get('sender', [''])[0])
                receiver_id = int(query_str_dict.get('receiver', [''])[0])
                latestchat_id = int(query_str_dict.get('latestchatid', [''])[0])

                if latestchat_id:
                    sql_str = "select * from chat_record where id>{latestchat_id} and ((sender={sender_id} and receiver={receiver_id}) or (sender={receiver_id} and receiver={sender_id}));".format(
                        latestchat_id=latestchat_id, sender_id=sender_id, receiver_id=receiver_id)

                cursor.execute(sql_str)
                result = cursor.fetchall()
                new_result = self.to_json(result)

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        content = json.dumps({"status": 0, "reason": '', "data": new_result})
        return ['{}'.format(content)]

    @onRequset(url="/user/record", method='POST')
    def postRecord(self, environ, start_response):

        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'POST'),
                                  ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')])

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test1234',
                                     db='chat',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                try:
                    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                except (ValueError):
                    request_body_size = 0
                # get data from mysql
                request_body = environ['wsgi.input'].read(request_body_size)
                request_body_dict = json.loads(request_body)
                request_body_data = request_body_dict.get('data')
                sender_id = request_body_data.get('sender')
                receiver_id = request_body_data.get('receiver')
                content = request_body_data.get('content')
                sendtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql_1 = "insert into chat_record (sender, receiver, sendtime, content) VALUES (%d,%d,'%s','%s');" % (
                    sender_id, receiver_id, sendtime, content)
                sql_2 = "select id from chat_record where id=(select max(id) from chat_record);"
                cursor.execute(sql_1)
                cursor.execute(sql_2)
                max_id = cursor.fetchall()[0].get('id')

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

        content = json.dumps({"status": 0, "reason": '', "currectid": max_id})
        return ['{}'.format(content)]
