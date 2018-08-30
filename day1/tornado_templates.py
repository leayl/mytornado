import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler, UIModule


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
        self.render('blog.html')

    def post(self, *args, **kwargs):
        pass

    def write_error(self, status_code, **kwargs):

        if status_code == 500:
            self.write('犯错了！！！')
        else:
            # 对于非500错误码，进行原来的错误提示
            super().write_error(status_code, **kwargs)


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        pass


class LoginModule(UIModule):
    def render(self, *args, **kwargs):
        # msg = self.get_query_argument('msg', None)
        msg = self.request.query
        r = ''
        if msg:
            r = '用户名或密码错误'
        return self.render_string('moduler/login_module.html', result=r)


class BlogModule(UIModule):
    def render(self, *args, **kwargs):
        blogs = [
            {
                'title': '第一篇博客',
                'tags': '情感　星座　生活',
                'author': '朱一龙的兄弟一号',
                'content': '朱一龙今天啃手指甲了吗？',
                'commit': 8,
                'avatar': 'ju1.jpeg',
            },
            {
                'title': '第二篇博客',
                'tags': '萌　星座　生活',
                'author': '朱一龙的兄弟二号',
                'content': '朱一龙今天萌混过关了吗？',
                'commit': 8,
                'avatar': 'ju2.jpeg',
            },
            {
                'title': '第三篇博客',
                'tags': '毛猴　星座　生活',
                'author': '朱一龙的兄弟三号',
                'content': '朱一龙今天看毛猴表情包了吗？',
                'commit': 0,
                'avatar': 'ju3.jpeg',
            },
            {
                'title': '第四篇博客',
                'tags': '游戏　饮品　生活',
                'author': '朱一龙的兄弟四号',
                'content': '朱一龙今天喝水溶C100了吗？',
                'commit': 8,
                'avatar': 'ju4.jpeg',
            },
        ]
        return self.render_string('moduler/blog_module.html', blogs=blogs)


class RegisterModule(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('moduler/register_module.html')


app = Application([
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/blog', BlogHandler), # 可以在后面以字典的方式传入初始化参数，在nitialize方法中接受处理
    ('/register', RegisterHandler),
],
    template_path='templates',
    static_path='statics',
    ui_modules={'loginmodule': LoginModule,
                'blogmodule': BlogModule,
                'registermodule': RegisterModule,
                }
)
server = HTTPServer(app)
define('port', type=int, default=8888)
parse_config_file('../config/conf')
server.listen(options.port)

IOLoop.current().start()