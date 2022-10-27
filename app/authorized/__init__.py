# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

authorized = Blueprint(
    'authorized_blueprint',
    __name__,
    url_prefix='/authorized',
    template_folder='templates',
    static_folder='static'
)
