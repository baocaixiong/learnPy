#!/usr/bin/env python
# coding: utf-8

from os import path
from platform import platform

DEBUG = True

ROOT_PATH = path.abspath(path.dirname('settings.py'))

TIME_ZONE = 'Asia/Shanghai'


LANGUAGE_CODE = 'zh-cn'

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
}

template_path = path.join(path.dirname(__file__), "templates")
static_path = path.join(path.dirname(__file__), "static")