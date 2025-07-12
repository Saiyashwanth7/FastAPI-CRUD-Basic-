from pydantic import computed_field, BaseModel


class UserProfile(BaseModel):
    name: str
    age: int
    weight: float
    height: float

    # creating a computed field called 'bmi'
    @computed_field(return_type=float)
    def bmi(self) -> float:
        b = round(self.weight / (self.height**2), 2)
        return b


profile = {"name": "Sai Yashwanth", "age": "21", "weight": 82.5, "height": 1.79}

p1 = UserProfile(**profile)


def read_user_profile(p: UserProfile):
    print(p.model_dump())
    print("BMI:", p.bmi)


read_user_profile(p1)
