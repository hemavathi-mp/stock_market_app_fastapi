import datetime
import logging

from sqlalchemy import update, func, or_

from task.config.db import SessionLocal

from task.models.model import Register, Order


class form:

    def login(email_or_mobile_no, password):
        with SessionLocal() as session:
            print("d",type(email_or_mobile_no))

            query = session.query(Register).filter(or_(Register.email == email_or_mobile_no,Register.mobile_no == email_or_mobile_no), Register.password==password).all()
            if len(query) != 0:
                return {"Login Successfully"}
            else:
                return {"Please enter valid email_id/mobile_no or password"}

    def insert(params):
        data = params.dict()
        if data['password'] != data['confirm_password']:
            return {'Entered password does not match'}

        with SessionLocal() as session:
            result = Register(**data)
            session.add(result)
            session.commit()
            session.refresh(result)

            return {"message":"Registration successful","user_id":result.id}

    def edit(registration_id, address):
        with SessionLocal() as session:

            db_user = session.query(Register).get(registration_id)
            if not db_user:
                return {"User not found"}
            u = update(Register).values({"address": address}).filter(Register.id == registration_id)
            session.execute(u)
            session.commit()

            # import uvicorn
            # from fastapi import FastAPI
            # from fastapi.encoders import jsonable_encoder
            # from pydantic import BaseModel
            #
            # app = FastAPI()
            #
            # class Product(BaseModel):
            #     name: str
            #     price: float
            #     inventory: int
            #
            # @app.patch("/posts/{id}", response_model=Product)
            # def patch_posts(id: int, post: Product):
            #     stored_data = post.dict()
            #     stored_model = Product(**stored_data)
            #     update_data = post.dict(exclude_unset=True)
            #     updated_data = stored_model.copy(update=update_data)
            #     post = jsonable_encoder(updated_data)
            #     return post

            return {"Address added succussfully"}

    def place_an_order(price, total_product,sale_or_not):
        with SessionLocal() as session:
            # assume total stock is 100
            # assume price for one product is 1000
            # sale_or_not 1 -> sold, 0 -> not sold
            total_stock = session.query(Order.stock).filter(Order.created_at.ilike(f'%{datetime.date.today()}%')).order_by(Order.stock.desc()).first()

            if total_stock[0] == None or total_stock[0] == 0:
                stock = 100
            else:
                stock = total_stock[0]

            if total_product > 100 or total_product > stock:
                raise ValueError('Out of stock')

            cost_price = 1000

            remaining_stock = stock - total_product
            print("s",stock,"remaining_stock",remaining_stock)
            actual_profit = total_product * cost_price
            order_profit = total_product * price

            if order_profit <= actual_profit:
                profit_loss = "loss"
                amount = order_profit
            else:
                profit_loss = "profit"
                amount = actual_profit
            print("D",remaining_stock)
            data = {
                 "stock":remaining_stock,
                 "profit_loss":profit_loss,
                "total_sale":sale_or_not,
                "price": amount,
                "total_product":total_product
             }

            result = Order(**data)
            session.add(result)
            session.commit()
            session.refresh(result)

            return {"message":"Order added successfully","order_id":result.id}

    def order_details():
        with SessionLocal() as session:
            total_stock = session.query(Order.stock).filter(Order.created_at.ilike(f'%{datetime.date.today()}%')).order_by(Order.stock.asc()).first()
            data = {
            "total_stock" : total_stock[0],
            "total_sale_of_the_day" : session.query(Order.total_sale).filter(Order.created_at.ilike(f'%{datetime.date.today()}%'), Order.total_sale==1).count(),
            "profit_or_loss" : session.query(Order.profit_loss).filter(Order.created_at.ilike(f'%{datetime.date.today()}%'),
                                                                           Order.profit_loss == "profit").count(),
            "new_order_list" : session.query(Order.id).filter(Order.created_at.ilike(f'%{datetime.date.today()}%')).count()
            }
            return data


    # def delete_task(task_id):
    #     with SessionLocal() as session:
    #         db_task = session.query(Task).get(task_id)
    #         if not db_task:
    #             raise HTTPException(status_code=404, detail="Task not found")
    #
    #         session.delete(db_task)
    #         session.commit()
    #         return {"ok": True}
    #






