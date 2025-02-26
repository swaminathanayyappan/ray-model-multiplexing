from ray import serve
from starlette.responses import JSONResponse
from starlette.requests import Request


@serve.deployment
class MultiplexerApp:
    async def __call__(self, http_request: Request) -> JSONResponse:
        if http_request.method.upper() == "GET":
            return JSONResponse({"message": "GET request received"})
        else:
            return JSONResponse({"message": "POST request received"})


app = MultiplexerApp.bind()