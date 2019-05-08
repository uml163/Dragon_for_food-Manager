# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,g,redirect
from common.models.User import ( User )
from common.libs.user.UserService import ( UserService )
from common.libs.Helper import ( ops_render )
from common.libs.UrlManager import ( UrlManager )
from application import app,db
import json

route_user = Blueprint( 'user_page',__name__ )

@route_user.route( "/login",methods = [ "GET","POST" ] )
def login():
    if request.method == "GET":
        if g.current_user:
            return  redirect( UrlManager.buildUrl("/") )
        return ops_render( "user/login.html")

    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    #flaskachemy 查询方法
    user_info = User.query.filter_by( login_name = login_name ).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "用户名或密码错误"
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd( login_pwd,user_info.login_salt ):
        resp['code'] = -1
        resp['msg'] = "用户名或密码错误"
        return jsonify(resp)
    # json.dumps()函数的使用，将字典转化为字符串
    response = make_response(json.dumps({'code': 200, 'msg': '登录成功~~'}))

    response.set_cookie( app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.geneAuthCode(user_info), user_info.uid),  60 * 60 * 24 * 120)  # 保存120天
    return response

@route_user.route( "/edit",methods = [ "GET","POST" ] )
def edit():
    #GET方法，显示用户界面
    if request.method == "GET":
        return ops_render( "user/edit.html",{ 'current':'edit' } )
    #定义统一json值
    resp = { 'code':200,'msg':'操作成功~','data':{} }
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''
    #参数判断
    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "姓名长度不能小于1～"
        return jsonify( resp )

    if email is None or len( email ) < 5:
        resp['code'] = -1
        resp['msg'] = "邮箱长度不能小于5～"
        return jsonify( resp )

    user_info = g.current_user
    #用户数据更新
    user_info.nickname = nickname
    user_info.email = email
    #用户数据提交
    db.session.add( user_info )
    db.session.commit()
    return jsonify(resp)


@route_user.route( "/reset-pwd",methods = [ "GET","POST" ] )
def resetPwd():
    if request.method == "GET":
        return ops_render( "user/reset_pwd.html",{ 'current':'reset-pwd' } )

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''


    if new_password is None or len( new_password ) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入，新密码和原密码不能相同哦~~"
        return jsonify(resp)

    user_info = g.current_user

    if user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "通用管理员，不能修改密码"
        return jsonify(resp)

    user_info.login_pwd = UserService.genePwd( new_password,user_info.login_salt )

    db.session.add( user_info )
    db.session.commit()
    #cookie刷新，在用户更新密码后同时更新cookie
    response = make_response(json.dumps( resp ))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 )  # 保存1天
    return response


@route_user.route( "/logout" )
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response