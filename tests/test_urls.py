import unittest

from webapp import create_app
from webapp.extensions import (
    db,
    admin,
    rest_api
)


class TestURLs(unittest.TestCase):
    # pass
    # 弥补 bug 的方法
    def setUp(self):

        admin._views = []
        rest_api.resources = []

        app = create_app('test')
        self.client = app.test_client()

        # 弥补 bug 的方法
        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_redirect(self):
        """ 检测根路径是否返回了302 """
        result = self.client.get('/')
        assert result.status_code == 302
        assert '/blog/' in result.headers['Location']


if __name__ == '__main__':
    unittest.main()
