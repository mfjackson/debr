import pandas as pd
from datetime import datetime
from pydantic import BaseModel, ValidationError, validator, parse_obj_as
from typing import Optional


class Users(BaseModel):
    login_uuid: str
    name_title: str
    name_first: str
    name_last: str
    gender: str
    email: str
    phone: str
    cell: str
    nat: str
    dob_date: datetime
    dob_age: int
    registered_date: datetime
    registered_age: int
    location_coordinates_latitude: float
    location_coordinates_longitude: float
    timezone_code: int

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(Users, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            return Exception(f"Value {df_value} in field {field} is null.")

        return df_value


class Media(BaseModel):
    login_uuid: str
    picture_large: str
    picture_medium: str
    picture_thumbnail: str

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(Media, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            raise Exception(f"Value {df_value} in field {field} is null.")

        return df_value


class Logins(BaseModel):
    login_uuid: str
    login_username: str
    login_salt: str
    login_sha256: str

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(Logins, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            raise Exception(f"Value {df_value} in field {field} is null.")

        return df_value


class AltIDs(BaseModel):
    login_uuid: str
    id_name: Optional[str] = None  # this is optional because it's returning Null in some cases
    id_value: Optional[str] = None  # this is optional because it's returning Null in some cases

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(AltIDs, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            return field.default

        return df_value


class Timezones(BaseModel):
    timezone_code: int
    location_timezone_offset: str
    location_timezone_description: str

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(Timezones, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            raise Exception(f"Value {df_value} in field {field} is null.")

        return df_value


class Countries(BaseModel):
    nat: str
    location_country: str

    @classmethod
    def from_dict(cls, d: dict):
        try:
            c = parse_obj_as(Countries, d)
            return c.__dict__
        except ValidationError as e:
            print(e.json())
            raise Exception(f"{d.get('name')} is the source of the ValidationError.")

    @validator('*', pre=True)
    def check_if_none(cls, df_value, field):
        if pd.isna(df_value):
            raise Exception(f"Value {df_value} in field {field} is null.")

        return df_value
