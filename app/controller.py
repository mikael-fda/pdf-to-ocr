#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, traceback, os
from flask import request, Response, send_file
from flask_restx import Resource, reqparse

from server import server, base_url, check_identity, redis_pdf_to_ocr
from common import Globals
from pdf_to_ocr import get_data

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

@nsAccount.route("/<string:username>")
class SendPDF(Resource):

    # create account
    def post(self, username):
        #if password != confirmation:
        #    raise Exception("Error verification passwords")
        dirPathIn = Globals.INPUT_FOLDER + username
        dirPathInOut = Globals.OUTPUT_FOLDER + username
        if not os.path.exists(dirPathIn) or not os.path.exists(dirPathInOut) :
            os.makedirs(dirPathIn)
            os.makedirs(dirPathInOut)
        return "Account created"

@nsPDF.route("/<string:username>/all")
class getAllPDF(Resource):
    # get All files path
    def get(self, username):
        dirPath = Globals.INPUT_FOLDER+ username
        if not os.path.isdir(dirPath):
            raise Exception("Error, you don't have any account")
        return get_data(username)
        #return [ x for x in os.listdir(dirPath)]

@nsPDF.route("/upload/<string:username>/<string:fileName>")
class checkPDF(Resource):
    def get(self, username, fileName):
        #check_identity()
        dirPath = Globals.INPUT_FOLDER+ username + "/" + fileName
        if not os.path.exists(dirPath):
            raise Exception("Error, you don't have any account")
        
        return send_file(dirPath, as_attachment=True)

@nsPDF.route("/upload/<string:username>")
class SendPDF(Resource):

    # upload pdf
    @nsPDF.expect(file_upload, validate=False)
    def put(self, username):
        """
        Upload your pdf
        """
        #check_identity()
        dirPath = Globals.INPUT_FOLDER + username
        if not os.path.exists(dirPath):
            raise Exception("Error, you don't have any account")
        
        args = file_upload.parse_args()
        file = args['file']
        filepath = dirPath + "/" + file.filename
        file.save(filepath)
        redis_pdf_to_ocr(username, filepath)
        return "file save ok"