from typing import List, Optional

from pydantic import BaseModel, root_validator

# schema
class register_form(BaseModel):
    mobile_no :int=None
    email :str=None
    name :str=None
    password :str=None
    confirm_password: str = None
    address: str = None

    # @root_validator()
    # def offer_validation(cls,values):
    #     pwd = values.get('password')
    #     confirm_pwd = values.get('confirm_password')
    #
    #     if pwd != confirm_pwd:
    #         raise ValueError('Entered password does not match')
