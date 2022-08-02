import unittest
import requests
from unittest.mock import patch

import app
import main

class TestMenuCommand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.documents.append({"type": "TEST", "number": "TEST", "name": "TEST"})
        app.directories.update({'TEST': ['TEST']})

    @patch('main.input', return_value = 'TEST')
    def test_search_person(self, mock_input):
        self.assertEqual(app.search_person(), "TEST")

    @patch('main.input', return_value = 'TEST')
    def test_search_shelf(self, mock_input):
        self.assertEqual(app.search_shelf(), "TEST")

    @patch('main.input', side_effect=['TEST1', 'TEST1', 'TEST1', 'TEST'])
    def test_new_document(self, mock_input):
        app.new_document()
        self.assertIn({"type": "TEST1", "number": "TEST1", "name": "TEST1"}, main.documents)
        self.assertIn("TEST1", app.directories['TEST'])
        app.documents.pop(-1)
        app.directories['TEST'] = ['TEST']

    @patch('main.input', return_value = 'TEST')
    def test_delete_document(self, mock_input):
        app.delete_document()
        self.assertNotIn({"type": "TEST", "number": "TEST", "name": "TEST"}, app.documents)
        self.assertNotIn("TEST", app.directories['TEST'])
        app.documents.append({"type": "TEST", "number": "TEST", "name": "TEST"})
        app.directories.update({'TEST': ['TEST']})

    @patch('main.input', side_effect=['TEST', 'TEST1'])
    def test_move_document(self, mock_input):
        app.directories.update({'TEST1': []})
        app.move_document()
        self.assertNotIn("TEST", app.directories['TEST'])
        self.assertIn("TEST", app.directories['TEST1'])
        app.directories.update({'TEST': ['TEST']})
        app.directories.pop('TEST1')

    @classmethod
    def tearDownClass(cls):
        app.documents.remove({"type": "TEST", "number": "TEST", "name": "TEST"})
        app.directories.pop('TEST')

class TestYandex(unittest.TestCase):
    token = ''

    def test_YaUploader_new_folder_1(self):

        uploader = main.YaUploader('TEST')
        result = uploader.new_folder()
        self.assertEqual("Папка на создана на Я.Диск", result)

    def test_YaUploader_new_folder_1_1(self):

        uploader = main.YaUploader('/TEST')
        result = uploader.new_folder()
        self.assertEqual("Ошибка 409, возможно папка уже существует, либо в названии папки есть /", result)

    def test_YaUploader_new_folder_2(self):

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': "disk:/"}
        result = requests.get(url, headers=headers, params=params).json()
        dirs = []
        for item in result['_embedded']['items']:
            if item['type'] == 'dir':
                dirs.append(item['name'])
        self.assertIn("TEST", dirs, 'Папка не была создана')


        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': "disk:/TEST"}
        requests.delete(url, headers=headers, params=params)

if __name__ == '__main__':
    unittest.main()