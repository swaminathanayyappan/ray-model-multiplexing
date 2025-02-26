from ray import serve
from transformers import pipeline
from starlette.requests import Request
from starlette.responses import JSONResponse


@serve.deployment(num_replicas=2)
class MultiplexerApp:
    def __init__(self):
        self.model_type = "translation_en_to_fr"

    @serve.multiplexed(max_num_models_per_replica=3)
    async def load_model(self, model_size: str) -> pipeline:
        """
        Function to load the translation model based on the model size

        Parameters
        ----------
            model_size: str
                Size of the model to be loaded in each serve replica
        Returns
        -------
            pipeline
                Translation pipeline model
        """
        return pipeline(self.model_type,
                        model=model_size)

    async def __call__(self, http_request: Request):
        """
        Function to handle the incoming HTTP request and return the translated
        text using the loaded translation model

        Parameters
        ----------
            http_request: Request
                Incoming HTTP request object
        Returns
        -------
            JSONResponse
                JSON response object with the translated text
        """
        model_id = serve.get_multiplexed_model_id()
        model: pipeline = await self.load_model(model_id)
        message, status_code = (None, 400)
        http_request_method: str = http_request.method.upper()
        http_request_body: dict = await http_request.json()
        if http_request_method == "POST":
            status_code = 200
            user_text: str = http_request_body.get("text", None)
            translation = model(user_text)
            message = {
                "translation": translation[0]["translation_text"],
                "model_size": model_id
            }
        else:
            message = {"error": "Invalid request method"}
        return JSONResponse(content=message, status_code=status_code)


app: serve.Application = MultiplexerApp.bind()
