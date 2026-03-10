from fastapi import FastAPI,Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app=FastAPI()


@app.get('/')
def health_check():
    return {"message":"Your API is working OK!"}


# Get Reqeust
@app.get("/posts/{p_id}")
def getPosts(p_id:str):
    return {"Post":'Here is you Post ID :{p_id}'}

# Here is the original shap of http method request with app fastapi  and the @app decoration it summrizing it in python decoration @app.get('route')
def getPostById(post_id:str):
    return {"Post":'Here is you Post ID :{post_id}'}
post=app.get("/post/{post_id}")(getPostById)
##=======================================================


## Post Requets
@app.post("/Post")
def Create_post(payload:dict = Body(...)):
    print(payload)
    return {"message":"Hello from post"}


######################################## New APIs ##################

class NewBrand(BaseModel):
    Brand:str
    Model:str

Car_Brands=[
    {
    "id":1,
    "Brand":"Toyota",
    "Model":"Yaris"
    },
    {
    "id":2,
    "Brand":"Volkswagen",
    "Model":"Golf"
    },
    {
    "id":3,
    "Brand":"Toyota",
    "Model":"Rav4"
    }
    ]

def get_index(brand_id:int):
    for  i,brand in enumerate(Car_Brands):
        if brand["id"]== brand_id:
            return i

def Get_one(id:int):
    for brand in Car_Brands:
        if brand.id==id:
            return brand
        else: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Brnad Found")
def delete_one(brand_id:int):
    for brand in Car_Brands:
        if brand["id"]==brand_id:
            Car_Brands.remove(brand)
            return brand

@app.get("/Brand")
def Get_All():
    return{"Data":Car_Brands}

@app.post("/Brand",status_code=status.HTTP_201_CREATED)
def Create_Brand(new_brand:NewBrand):
    append_Brand=new_brand.model_dump()
    append_Brand['id']=randrange(1,1000)
    Car_Brands.append(append_Brand)
    return{ "Data":append_Brand}

@app.get('/Brand/{Brand_id}')
def Get_by_Brand_Id(Brand_id:int):
    Car_Brand=Get_one(Brand_id)
    return {"Data":Car_Brand}

@app.delete("/Brand/{id}")
def delete_Brand(id:int):
   deleted_brand= delete_one(id)
   return{"Deleted_data":deleted_brand}

@app.put("/Brand/{id}")
def update_brand(id:int,brand:NewBrand):
    brand_index=get_index(id)
    brand_dict= brand.model_dump()
    brand_dict["id"]=id
    Car_Brands[brand_index]=brand_dict
    return {"data":Car_Brands}