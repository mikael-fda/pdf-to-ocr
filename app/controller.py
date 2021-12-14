#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, traceback, os
from flask import request, Response, send_file
from flask_restx import Resource, reqparse

from handler import *
from server import server, base_url, check_identity
from common import Globals
from sql import get_user, get_file, insert_file, insert_user
from redis_queue import redis_pdf_to_ocr

from errors import ObjectNotFound, AccountError, ObjectBadFormat
from werkzeug.datastructures import FileStorage
import logging

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
    
    # Create account
    def post(self, user_name, user_mail):
        """
        Create your account
        """
        dirPathIn = Globals.INPUT_FOLDER + user_name
        dirPathInOut = Globals.OUTPUT_FOLDER + user_name
        db_user_name = insert_user(user_name, user_mail)
        if not os.path.exists(dirPathIn) or not os.path.exists(dirPathInOut) :
            os.makedirs(dirPathIn)
            os.makedirs(dirPathInOut)
        else:
            raise AccountError("Your Account already exist")
        return { "Creation": "Sucess", "user_name" : db_user_name}

@nsAccount.route("/<string:user_name>")
class GetUser(Resource):
    # list account
    def get(self, user_name):
        """
        See your account informations
        """
        return get_user(user_name)

@nsPDF.route("/<string:user_name>/_all")
class getAllPDF(Resource):
    # get All files path
    def get(self, user_name):
        """
        See all of your files ready to download
        """
        user = get_user(user_name)
        files = get_file(user_name)
        files = [x[3] for x in files]
        data = list(set(files))
        return [x.split("/")[-1] for x in data]

@nsPDF.route("/download/<string:user_name>/<string:file_name>")
class checkPDF(Resource):
    def get(self, user_name, file_name):
        """
        Download one of your files
        """
        user = get_user(user_name)
        files = get_file(user_name)
        dirPath = Globals.OUTPUT_FOLDER + user_name + "/" + file_name
        if not os.path.exists(dirPath):
            raise ObjectNotFound("Error during your files transformation, please reupload your .pdf file")
        
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
        user = get_user(user_name)
        
        args = file_upload.parse_args()
        file = args['file']
        if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
            raise ObjectBadFormat("You only can upload .pdf files")
        file_path = dirPath + "/" + file.filename
        file.save(file_path)

        redis_pdf_to_ocr(user_name, file_path)

        return "File save Success !", 200