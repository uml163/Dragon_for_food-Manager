# -*- coding: utf-8 -*-
from flask import request,g
from application import app,db
import json
from common.libs.Helper import getCurrentDate
from common.models.log.AppAccessLog import AppAccessLog
from common.models.log.AppErrorLog import AppErrorLog

class LogService():
    @staticmethod
    def addAccessLog():
        AccessLog = AppAccessLog()
        AccessLog.target_url = request.url
        AccessLog.referer_url = request.referrer
        AccessLog.ip = request.remote_addr
        AccessLog.query_params = json.dumps(  request.values.to_dict() )
        if 'current_user' in g and g.current_user is not None:
            AccessLog.uid = g.current_user.uid
        AccessLog.ua = request.headers.get( "User-Agent" )
        AccessLog.created_time = getCurrentDate()
        db.session.add( AccessLog )
        db.session.commit( )
        return True

    @staticmethod
    def addErrorLog( content ):
        if 'favicon.ico' in request.url:
            return
        ErrorLog = AppErrorLog()
        ErrorLog.target_url = request.url
        ErrorLog.referer_url = request.referrer
        ErrorLog.query_params = json.dumps(request.values.to_dict())
        ErrorLog.content = content
        ErrorLog.created_time = getCurrentDate()
        db.session.add(ErrorLog)
        db.session.commit()
        return True