#!/usr/bin/env python3

import unittest
import unittest.mock
import json
import os.path as path


class TestWeb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Init test app """
        app = web_app.get_application(Config)
        cls.app = app.test_client()
        cls.context = Context(Config)

    def get(self, url):
        """ :returns: utf8 string, containig html code of url. """
        return self.app.get(url).data.decode('utf8')

    def get_json(self, url):
        """ :returns: dict. """
        data_text = self.get(url)
        return json.loads(data_text)

    def get_and_check(self, url):
        """ :returns: utf8 string and check not 404. """
        html = self.get(url)
        self.assertNotIn('404 Not Found', html)
        return html

    def post_json(self, url: str, data_dict: dict) -> str:
        response = self.app.post(url, data=json.dumps(data_dict),
                                 follow_redirects=True,
                                 content_type ='application/json')
        return response.data.decode('utf8')

    def test_index(self):
        """ Web: get main page. """
        main_page = self.get_and_check('/')
        self.assertIn('CRM', main_page)

    def test_save_config(self):
        """ Web: rest save config rest request. """
        res = self.post_json(
            '/api/save_config/',
             {'recipients': 'test_recipients',
              'html_template': 'test_html'
             })
        response = json.loads(res)
        self.assertTrue(response['success'])
        self.assertTrue(path.isfile(self.context.recipients))
        self.assertEqual(self.context.get_recipients(), 'test_recipients')
        self.assertEqual(self.context.get_html_template(), 'test_html')

    @unittest.mock.patch('os.system')
    def test_commands(self, system_patch):
        """ Web: rest save config rest request. """
        res = self.post_json('/api/command/', {'command': 'generate'})
        response = json.loads(res)
        self.assertTrue(response['success'])
        self.assertTrue(system_patch.called)

    def test_get_log(self):
        """ Web: get log."""
        log = self.get('/api/get_log/')
        self.assertTrue(log)

