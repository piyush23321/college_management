from typing import List
from pydantic import BaseModel


class Create_User_request(BaseModel):
    name: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class ResetPassword(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    type: str


class StudentCreate(BaseModel):
    name: str
    college_code: str
    enroll_num: str


class StudentData(BaseModel):
    id: int
    name: str
    enroll_num: str


class CollegesRead(BaseModel):
    id: int
    name: str
    score: int
    city_id: int
    state_id: int
    college_code: str
    students: List[StudentData]