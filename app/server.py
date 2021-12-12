#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask, Blueprint, url_for, redirect
from flask_restx import Api

base_url = "/project/pfd_to_odt"

class Server:

    authorizations = {
        "apikey": {
            "type": "username",
            "in": "header",
            "name": "X-c4token",
            "description": "Token of your tenant_id"
        }
    }

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = True
        self.app.config['JSON_SORT_KEYS'] = False

        blueprint = Blueprint('api', __name__, url_prefix=base_url)
        self.api = Api(
            app=blueprint,
            title='Project PDF to OCR',
            version='1.0',
            description='Change your PDF files to OCR files',
            authorizations=self.authorizations,
            security='apikey'
        )
        self.app.register_blueprint(blueprint)

    def run(self):
        self.app.run()

server = Server()

@server.app.route('/status')
def status():
    return 'OK'

@server.app.route('/')
def index():
    return redirect(base_url)

def check_identity():
    if not "username" in request.headers or not "password" in request.headers:
        raise Exception("You are not connected")