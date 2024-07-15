from fastapi import FastAPI 


from views.hello import router as hello_router
from views.items import router as item_router
from views.secret_views import router as secret_router
from views.users.views import router as users_router


app = FastAPI()
app.include_router(users_router)
app.include_router(hello_router)
app.include_router(item_router)
app.include_router(secret_router)    




@app.get("/")
def hello_root():
    return {"message": "Hello"}




