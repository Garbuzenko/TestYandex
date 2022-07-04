import json

import time
import uuid
from unittest.mock import patch

import pytest as pytest

import VkSession
import YaUploader
import input_utils

FIXTURE = [
    ('dir1', "file_name", "https://theblueprint.ru/upload/24954/logo.png"),
    ('dir1', "file_name2", "https://theblueprint.ru/upload/24954/logo.png")
]

class TestPytest:

    def setup(self):
        print('setup 1')
        [token_ya, token_vk] = input_utils.get_tokens()
        self.ya = YaUploader.YaClass(token_ya, "netology")
        self.vk = VkSession.VkClass(token_vk)
        print('setup 2')
    @pytest.mark.parametrize("dir, file_name, href", FIXTURE)
    def test_commands_logic(self, dir, file_name, href):
        mydir = dir + str(uuid.uuid4())
        self.ya.create_dir(mydir)
        path_to_file = "{0}/{1}".format(mydir, file_name)
        ya_href = self.ya.get_href_for_upload(path_to_file, href=href)  # Получим ссылку для загрузки файла
        assert self.ya.upload(href=ya_href) == 200 # Выполним загрузку
        time.sleep(1)  # Подождем загрузку последнего файла
        res = ','.join(self.ya.get_meta(mydir, only_name=1))
        print("res=", res)
        assert res == file_name

