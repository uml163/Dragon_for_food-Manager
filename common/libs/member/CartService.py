# -*- coding: utf-8 -*-
#购物车功能实现
from application import db
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate
class CartService():

    @staticmethod
    def deleteItem( member_id = 0,items = None ):
        if member_id < 1 or not items:
            return False
        for item in items:
            MemberCart.query.filter_by( food_id = item['id'],member_id = member_id ).delete()
        db.session.commit()
        return True

    @staticmethod
    def setItems( member_id = 0,food_id = 0,number = 0 ):
        #if member_id < 1 or food_id < 1 or number < 1:
            #return False
        cart_info = MemberCart.query.filter_by( food_id = food_id, member_id= member_id ).first()
        if cart_info:
            MemberCart_model = cart_info
        else:
            MemberCart_model = MemberCart()
            MemberCart_model.member_id = member_id
            MemberCart_model.created_time = getCurrentDate()

        MemberCart_model.food_id = food_id
        MemberCart_model.quantity = number
        MemberCart_model.updated_time = getCurrentDate()
        db.session.add(MemberCart_model)
        db.session.commit()
        return True

