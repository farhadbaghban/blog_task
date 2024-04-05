from fastapi import FastAPI
import uvicorn
from router.users import router as user_router
from db.engine import Base, engine

app = FastAPI()
app.include_router(user_router, prefix="/users")

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
