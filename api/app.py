from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path
from src.api.resolvers import query

type_defs = load_schema_from_path("src/api/schema.graphql")
schema = make_executable_schema(type_defs, query)

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))

@app.get("/health")
def health():
    return {"status": "ok"}
