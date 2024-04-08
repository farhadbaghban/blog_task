from fastapi import FastAPI
import uvicorn
from router.users import router as user_router
from router.posts import router as post_router
from db.engine import Base, engine

app = FastAPI()
app.include_router(user_router, prefix="/users")
app.include_router(post_router, prefix="/posts")
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
