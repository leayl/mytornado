from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import UIModule

from day1.app.myapp import MyAppliction
from day1.app.myhandler import IndexHandler, LoginHandler, BlogHandler, RegisterHandler
from day1.app.mymoduler import LoginModule, BlogModule, RegisterModule
from day1.app.settings import settings

app = MyAppliction([
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/blog', BlogHandler), # 可以在后面以字典的方式传入初始化参数，在nitialize方法中接受处理
    ('/register', RegisterHandler),
],
    tp='templates',
    sp='statics',
    um={'loginmodule': LoginModule,
        'blogmodule': BlogModule,
        'registermodule': RegisterModule,
                })
server = HTTPServer(app)
server.listen(settings['port'])

IOLoop.current().start()