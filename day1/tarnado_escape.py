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
        self.render('escape.html', result='')

    def post(self, *args, **kwargs):
        t = self.get_body_argument('test')
        # 针对chrom浏览器的转义
        self.set_header('X-XSS-Protection', 0)

        self.render('escape.html', result=t)


# 定义配置文件中的内容result
define('port', type=int, default=8888)
# 指定配置文件路径
parse_config_file('../config/conf')


app = Application([('/', IndexHandler)],
                  template_path='templates',
                  )
# 创建真正的服务器程序
server = HTTPServer(app)
server.listen(options.port) # 从配置文件中读取port

# 启动服务器
IOLoop.current().start()

