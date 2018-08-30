import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')


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
            # self.set_status(888, 'funny') # 手动设置相应行状态码,不轻易自己设置
            # self.write('welcome to blog')

            # 生成一个错误页面,参数为状态码
            # self.send_error(404) # 传递给write_error方法
        # 获取自定义请求头
        # print(self.request.headers.get('myhead', None))


            # 返回json字符串作为服务器的响应
            # 第一步，构建字典，把要返回的内容作为字典的键值对
            resp = {'key1': 'value1',
                    'key2': 'value2'
                    }
            # # 第二步，把字典转化为JSON字符串
            # jsonstr = json.dumps(resp)
            # # 第三步，将JSON字符串作为服务器相应发送给客户端
            # self.set_header('Content-Type','apolication/json;charset=UTF-8')
            # self.write(jsonstr)
            # # 请求头格式Content-Type:text/html

            # 也可跳过二三步，直接返回resp,tornado会自动解析
            self.write(resp)
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
], template_path='templates')
server = HTTPServer(app)
define('port', type=int, default=8888)
parse_config_file('../config/conf')
server.listen(options.port)

IOLoop.current().start()