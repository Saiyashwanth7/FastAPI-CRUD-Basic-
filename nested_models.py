from pydantic import BaseModel,EmailStr

class Address(BaseModel):
    city:str
    state:str 
    pin:str
    
class UserProfile(BaseModel):
    name:str 
    age:int
    email:EmailStr
    address:Address
    
profile={
    "name":"Sai Yashwanth",
    "age":"21",
    "email":"saiyashwanthdasari@gmail.com",
    "address":{"city":"karimnagar","state":"Telangana","pin":"505001"}
}

p1=UserProfile(**profile)

print(p1)