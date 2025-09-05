from experimental.routes import router_experimental
from fastapi import FastAPI
from fastapi.testclient import TestClient

appExp = FastAPI()
client = TestClient(appExp)

appExp.include_router(router_experimental)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(appExp, host="0.0.0.0", port=8001)