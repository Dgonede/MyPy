__all__ = ("app",)

from app import app   
import uvicorn




if __name__=="__main__":
    uvicorn.run("main:app", reload=True)


