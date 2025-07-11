from fastapi import FastAPI
from pydantic import EmailStr, Field, field_validator, BaseModel
from typing import Annotated

app = FastAPI()


class UserProfile(BaseModel):
    name: str = Field(max_length=50)
    age: Annotated[int, Field(gt=0, lt=120)]
    email: EmailStr

    @field_validator("email")
    @classmethod
    def email_validation(cls, value):
        valid_domain = ["hdfc.com", "icici.com", "gmail.com"]
        domain = value.split("@")[-1]
        if domain in valid_domain:
            return value
        else:
            raise ValueError("Invalid domain of the mail")

    @field_validator("name")
    @classmethod
    def name_validation(cls, value):
        return value.upper()

    """Apparently the field_validation is linked with the automatic type coercion of the pydantic ,
    So this field_validation can be performed in two modes, i.e.
    one mode='before' -> before tyep coercion and 
    mode='after' -> after the type coercion. Default will be mode='after' """

    @field_validator("age", mode="before")
    @classmethod
    def age_validation(cls, value):
        if 0 < value < 120:
            return value
        else:
            raise ValueError("The age value type should be int not str ")

    # this above function would raise error if age is in str ,or just use mode='after' to avoid errors


profile = {
    "name": "Dasari Sai Yashwanth",
    "age": 21,
    "email": "saiyashwanthdasari@gmail.com",
}

p = UserProfile(**profile)


def read_profile(user_profile: UserProfile):
    print(user_profile.model_dump())


read_profile(p)
