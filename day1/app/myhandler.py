from os import remove

import time
from tornado.web import RequestHandler

from day1.utils.mdutil import mymd5


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        result = ''
        if self.get_query_argument('msg',None):
            result = '用户名或密码错误'
        self.render('login.html', result=result)

    def post(self, *args, **kwargs):
        pass


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        password = self.get_body_argument('password', None)
        password = mymd5(password)
        result = self.application.dbutil.login(username, password)
        if result:
            self.redirect('/blog?username={}'.format(username))
        else:
            msg = 'fail'
            self.redirect('/?mag={}'.format(msg))


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        city = self.get_body_argument('city')
        # 对用户在注册页面中输入的password进行md5转码
        password = mymd5(password)
        if username and password and city:
            avatar = None
            if self.request.files:
                file = self.request.files['avatar'][0]
                # 防止文件名重复被覆盖
                file_name = str(time.time()) + file['filename']
                avatar = file_name
                body = file['body']
                writer = open('statics/images/'+file_name, 'wb')
                writer.write(body)
                writer.close()

            try:
                self.application.dbutil.save(username=username, password=password,
                            city=city, avatar=avatar)
                self.redirect('/')
            except Exception as e:
                if avatar:
                    remove('statics/images/'+avatar)
                self.redirect('/register?msg='+str(e))
        else:
            self.redirect('/register?msg=empty')


class BlogHandler(RequestHandler):
    def set_default_headers(self):
        # 设置默认的响应头
        print('set_default_headers方法调用')

    def initialize(self):
        # 接受路由列表中的初始化参数
        pass

    def on_finish(self):
        # 如果在生成相应内容时有一些资源需要去关闭或释放
        # 可在这里面进行
        pass

    def get(self, *args, **kwargs):
        self.render('blog.html')

    def post(self, *args, **kwargs):
        pass

    def write_error(self, status_code, **kwargs):

        if status_code == 500:
            self.write('犯错了！！！')
        else:
            # 对于非500错误码，进行原来的错误提示
            super().write_error(status_code, **kwargs)