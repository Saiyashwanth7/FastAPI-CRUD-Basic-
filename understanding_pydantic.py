# In this I'm trying to learn and understand Pydantic from nitish singh's video lectures (campusx )
# As of now I have learnt about the type validations in the Pydantic and how it helps python in concurring type validation

from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import *

# Created a Pydantic model (nothing but a class with BaseModel as its parameter) for User profile
class UserProfile(BaseModel):
    name: Annotated[str,Field(max_length=50,title="Name of the user",description="Description ")]
    age: Annotated[int,Field(gt=0,lt=100,strict=True)]
    gender: Annotated[str,Field(max_length=1,default="Others",description="M or F")]
    country: Annotated[Optional[str],Field(default=None,description="Name your country")]
    hobbies: Annotated[Optional[List[str]],Field(default=None,max_length=10,description="Any hobbies...?")]
    contact_number: Annotated[Optional[str],Field(default=None,description="Enter your mobiole number")]

# In this below line of code we are creating a blue print kind of data for the user profile data
profile = {
    "name": "Sai Yashwanth",
    "age": 21,
    "gender": "M",
    "country": "India",
    "hobbies": ["Hobbies","1","2","3"],  # the keys in the dict must be same as the variables set in the pydantic model
    # here Pydantic raised an error cause i initially used "Hobbies" instead of "hobbies"
    
}

# now lets give the above raw input to the pydantic model and initiate it as an object (p1 in this case) ,here ** is used to extract the dictionary elements
p1 = UserProfile(**profile)


def reading_user_profile(p: UserProfile):
    print(p.name)
    print(p.age)
    print(p.country)
    print(p.gender)
    print(p.hobbies)
    print(p.contact_number)

reading_user_profile(p1)
