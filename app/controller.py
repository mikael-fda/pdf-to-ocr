#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, traceback, os
from flask import request, Response, send_file
from flask_restx import Resource, reqparse

from server import server, base_url, check_identity, redis_pdf_to_ocr
from common import Globals
from sql import *

from werkzeug.datastructures import FileStorage

file_upload = reqparse.RequestParser()
file_upload.add_argument('file', location='files',type=FileStorage, required=True)

app, api = server.app, server.api

nsAccount = api.namespace(
    name='account',
    description='Create your account'
)

nsPDF = api.namespace(
    name='PDF',
    description='Upload or Download your PDF and OCR files'
)

@nsAccount.route("/<string:user_name>/<string:user_mail>")
class CreateUser(Resource):
    # create account
    def post(self, user_name, user_mail):
        #if password != confirmation:
        #    raise Exception("Error verification passwords")
        dirPathIn = Globals.INPUT_FOLDER + user_name
        dirPathInOut = Globals.OUTPUT_FOLDER + user_name
        id_user = insert_user(user_name, user_mail)
        if not os.path.exists(dirPathIn) or not os.path.exists(dirPathInOut) :
            os.makedirs(dirPathIn)
            os.makedirs(dirPathInOut)
        return { "Creation": "Sucess", "user_name" : id_user}

@nsAccount.route("/<string:user_name>")
class GetUser(Resource):
    # list account
    def get(self, user_name):
        return get_user(user_name)

@nsPDF.route("/<string:user_name>/all")
class getAllPDF(Resource):
    # get All files path
    def get(self, user_name):
        dirPath = Globals.INPUT_FOLDER + user_name
        if not os.path.isdir(dirPath):
            raise Exception("Error, you don't have any account")
        return get_file(user_name)

@nsPDF.route("/download/<string:user_name>/<string:fileName>")
class checkPDF(Resource):
    def get(self, user_name, fileName):
        #TODO recup chemin via bd
        #check_identity()
        dirPath = Globals.INPUT_FOLDER+ user_name + "/" + fileName
        if not os.path.exists(dirPath):
            raise Exception("Error, you don't have any account")
        
        return send_file(dirPath, as_attachment=True)

@nsPDF.route("/upload/<string:user_name>")
class SendPDF(Resource):

    # upload pdf
    @nsPDF.expect(file_upload, validate=False)
    def put(self, user_name):
        """
        Upload your pdf
        """
        dirPath = Globals.INPUT_FOLDER + user_name
        if not os.path.exists(dirPath):
            raise Exception("Error, you don't have any account")
        
        args = file_upload.parse_args()
        file = args['file']
        filepath = dirPath + "/" + file.filename
        file.save(filepath)
        redis_pdf_to_ocr(user_name, filepath)
        return "file save ok"