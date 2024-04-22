import logging

from fastapi import APIRouter, Request, Depends

from task.controller.task_controller import form
from task.schema.registration import register_form

router = APIRouter(
    prefix='/new_task',
    tags=["new_task API's"],
)

# login api
@router.post('/login')
def login(email_or_mobile_no:str, password:str):
    result = form.login(email_or_mobile_no, password)
    return {"success": "OK", "message": "Login Form", "data": result}

# Registration form: Add user details
@router.post('/add')
async def add(data: register_form):
    result = form.insert(data)
    return {"success": "OK", "message": "Registration Form", "data": result}

@router.patch('/add_address')
async def edit(registration_id: int,address:str):
    result = form.edit(registration_id,address)
    return {"success": "OK", "message": "address added successfully", "data": result}


@router.post('/order')
async def order(price :int=None,total_product :int=None, sale_or_not:int=0):
    # sale_or_not is True if the product is sale otherwise False
    result = form.place_an_order(price,total_product,sale_or_not)
    return {"success": "OK", "message": "Order added successfully", "data": result}


# order_details api return data which is need to be display on dashboard, this api should call after "order" api is called.
@router.get('/order_details')
async def order_details():
    result = form.order_details()
    return {"success": "OK", "message": "List order details", "data": result}

# @app.delete("/task_delete/{task_id}")
# def delete_hero(task_id: int):
#     result = form.delete_task(task_id)
#     return {"success": "OK", "message": "Task is successfully deleted", "data": result}

