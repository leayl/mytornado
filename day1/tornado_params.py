from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        msg = self.get_query_argument('msg', None)
        if msg == 'fail':
            html = '<form method="post" action=/login>' \
             '<span>用户名：</span><input type="text" name=username><br>' \
             '<span>密码：</span><input type="password" name = password><br>' \
             '<input type="submit" value=提交>&nbsp;&nbsp;&nbsp;&nbsp;' \
             '<input type="reset" value=重置>' \
             '<p>用户名或密码错误</p>' \
             '</form>'
        else:
            html = '<form method="post" action=/login enctype=multipart/form-data>' \
             '<span>用户名：</span><input type="text" name=username><br>' \
             '<span>密码：</span><input type="password" name = password><br>' \
             '<input type=file name=avatar><br>' \
             '<input type=file name=avatar><br>' \
             '<input type="submit" value=提交>&nbsp;&nbsp;&nbsp;&nbsp;' \
             '<input type="reset" value=重置>' \
             '</form>'

        self.write(html)

    def post(self, *args, **kwargs):
        pass


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        password = self.get_body_argument('password', None)

        if username == 'abc' and password == '123':
            # 如果用户上传了图片，则保存图片
            # HTTPServerRequest对象的files属性
            # 以字典的方式组织上传文件,{key1:[file1,file2,...],...}
            # 如果未上传文件，为{}
            files = self.request.files
            if files:
                avatars = files.get('avatar')
                for avatar in avatars:
                    # 上传文件有三个属性：
                    # type：文件类型
                    # filename：文件的原始名字
                    # body：该文件的内容（二进制格式）
                    body = avatar.get('body')
                    filename = avatar.get('filename')
                    # 将body写入一个文件，进行保存
                    writer = open('../upload/{}'.format(filename), 'wb')
                    writer.write(body)
                    writer.close()
            self.redirect('/blog?username='+username)
        else:
            self.redirect('/?msg=fail')


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
        username = self.get_query_argument('username', None)
        if username:
            self.write('welcome '+username)
        else:
            self.set_status(888, 'funny') # 手动设置相应航状态码,不轻易自己设置
            self.write('welcome to blog')

            # 生成一个错误页面,参数为状态码
            self.send_error(404) # 传递给write_error方法
        # 获取自定义请求头
        print(self.request.headers.get('myhead', None))

    def post(self, *args, **kwargs):
        pass

    def write_error(self, status_code, **kwargs):

        if status_code == 500:
            self.write('犯错了！！！')
        else:
            # 对于非500错误码，进行原来的错误提示
            super().write_error(status_code, **kwargs)

app = Application([
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/blog', BlogHandler), # 可以在后面以字典的方式传入初始化参数，在nitialize方法中接受处理
])
server = HTTPServer(app)
define('port', type=int, default=8888)
parse_config_file('../config/conf')
server.listen(options.port)

IOLoop.current().start()