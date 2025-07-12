from pydantic import BaseModel, EmailStr, model_validator


class UserProfile(BaseModel):
    name: str
    email: EmailStr
    age: int
    employed: bool

    @model_validator(mode="after")
    def age_occupation(cls, model):
        if model.age > 60 and model.employed:
            raise ValueError("Exceeded reitrement limit")
        return model


profile = {
    "name": "Sai Yashwanth",
    "email": "saiyashwanthdasari@gmail.com",
    "age": "21",
    "employed": False,
}

p1 = UserProfile(**profile)


def read_profile(p: UserProfile):
    print(p.model_dump())


read_profile(p1)
