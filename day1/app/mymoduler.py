from tornado.web import UIModule


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
        r = ''
        q = self.request.query
        print(q)
        if q:
            q = q.split('=')[1]
            if q == 'empty':
                r = '请输入完整信息'
            elif q == 'error':
                r = '服务器繁忙，请稍后重试'
            elif q == 'duplicate':
                r = '该用户名已被注册'
        return self.render_string('moduler/register_module.html', result=r)
