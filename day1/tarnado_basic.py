import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler


# １.创建Tornado服务器
# 继承子RequestHandler类
# 对请求的方式（get/post）作出相应,调用重写父类的get/post方法做出相应
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('<a href=/python>Hello Python</a><br>')


    def post(self, *args, **kwargs):
        pass

class PythonHandler(RequestHandler):
    def get(self,  p1=None, p2=None, *args, **kwargs):
        self.write('hello python <br>')
        if p1:
            self.write('date:' + p1 + '<br>')
        if p2:
            self.write('subject:' + p2 + '<br>')

    def post(self, *args, **kwargs):
        pass
# 定义配置文件中的内容
define('port', type=int, default=8888)
# 指定配置文件路径
parse_config_file('../config/conf')

# 创建Application对象，Application是Tornado最核心的类
# 所有关于服务器的配置信息都要写在Application构造器中
# 以构造器的参数形式传入
# 比如：路由列表
# 路由列表的作用是告诉Tornado，对特定路径的请求，由哪个类进行响应
app = Application([('/', IndexHandler),
                   ('/python', PythonHandler),
                   ('/python/([0-9a-zA-Z]+)', PythonHandler),
                   ('/python/([0-9a-zA-Z]+)/([a-zA-Z]+)', PythonHandler),
                   ])
# 创建真正的服务器程序
server = HTTPServer(app)
server.listen(options.port) # 从配置文件中读取port

# 启动服务器
IOLoop.current().start()

