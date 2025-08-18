# -*- coding: utf-8 -*-
import os

name        = "lame"
version     = "3.100"
authors     = ["M83"]
description = "LAME MP3 인코더 라이브러리"

build_requires = [
    "gcc-11.5.0",
    "python-3.13.2",   # Python 버전을 3.13.2 로 통일
]

build_command = "python {root}/rezbuild.py install"

def commands():
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")
    env.LIBRARY_PATH.append("{root}/lib")

