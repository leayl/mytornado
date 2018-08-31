from tornado.web import Application

from day1.utils.dbutil import DBUtil


class MyAppliction(Application):
    def __init__(self, handlers, tp, sp, um):
        super().__init__(handlers, template_path=tp,
                         static_path=sp, ui_modules=um)
        self.dbutil = DBUtil()