# -*- coding: utf-8 -*-
from application import db
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from common.models.food.Food import Food
from common.libs.Helper import getCurrentDate
class FoodService():

    @staticmethod
    def setStockChangeLog( food_id = 0,quantity = 0,note = '' ):

        if food_id < 1:
            return False

        food_info = Food.query.filter_by( id = food_id ).first()
        if not food_info:
            return False

        FoodStockChangeLog_model = FoodStockChangeLog()
        FoodStockChangeLog_model.food_id = food_id
        FoodStockChangeLog_model.unit = quantity
        FoodStockChangeLog_model.total_stock = food_info.stock
        FoodStockChangeLog_model.note = note
        FoodStockChangeLog_model.created_time = getCurrentDate()
        db.session.add(FoodStockChangeLog_model)
        db.session.commit()
        return True


