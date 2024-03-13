from contextlib import asynccontextmanager
from api.api_router import api_router
from config import settings
from db import sessionmanager
from starlette_graphene3 import GraphQLApp, make_playground_handler
from random import randint
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from gql import gql_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Library",
    docs_url="/api/docs")

app.add_middleware(
    SessionMiddleware,
    secret_key=f"{randint(1000, 4000)}-secret-string-{randint(1000, 4000)}",

)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

app.mount("/", GraphQLApp(
    schema=gql_schema,
    on_get=make_playground_handler()
))

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=False
#     )
