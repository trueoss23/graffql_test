import strawberry


from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.asgi import GraphQL


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/graphql")
async def graphql_endpoint():
    return GraphQL(schema)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
