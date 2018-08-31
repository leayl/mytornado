import pymysql
from os import remove


class DBUtil:
    def __init__(self, **kwargs):
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 3306)
        user = kwargs.get('user', 'root')
        password = kwargs.get('password', '123456')
        database = kwargs.get('database', 'myblog')
        charset = kwargs.get('database', 'utf8')
        s = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset,
        }
        connection = pymysql.connect(**s)
        if connection:
            self.cursor = connection.cursor()
        else:
            raise Exception('数据库参数异常')

    def login(self, username, password):
        sql = 'select count(*) from tb_user WHERE user_name=%s and user_password=%s'
        params = (username, password)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def save(self, **kwargs):
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        city = kwargs.get('city', None)
        avatar = kwargs.get('avatar', None)

        if username and password and city:
            sql = 'insert into tb_user(user_name, user_password, user_avatar, user_city) VALUES (%s,%s,%s,%s);'
            params = (username, password, avatar, city)
            try:
                self.cursor.execute(sql, params)
                self.cursor.connection.commit()
            except Exception as e:
                msg = 'dberror'
                info = str(e)
                error_code = info.split(',')[0].split('(')[1]
                if error_code == '1062':
                    msg = 'duplicate'
                raise Exception(msg)
