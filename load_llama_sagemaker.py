"""
Author: Temiloluwa Adeoti
Description: Classes to load llama models from
             Sagemaker inference endpoints and use with langchain
Date: 27-08-2023



# Sample payload for llama language model

payload = {
            "inputs": "Who is the president of Nigeia?",
            "parameters": {
                "max_new_tokens": 64,
                "top_p": 0.9,
                "temperature": 0.6,
                "return_full_text": False,
            }
        }

# sample payload for llama chat model 
payload = {
    "inputs": [
        [
            {
                "role": "system",
                "content": "You are a kind robot."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    ],
    "parameters": model_kwargs
}
"""


import json
from typing import Dict
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        payload = {
            "inputs": prompt,
            "parameters": model_kwargs
        }
        input_str = json.dumps(payload)
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generation"]



class LLamaModel(SagemakerEndpoint):
    def __init__(self,
        endpoint_name: str = None,
        credentials_profile: str = None,
        content_handler: ContentHandler = ContentHandler(),
        max_new_tokens: int = None,
        top_p: float = None,
        temperature: float = None,
        return_full_text: bool = False):

        model_kwargs = {
            "max_new_tokens": max_new_tokens,
            "top_p": top_p,
            "temperature": temperature,
            "return_full_text": return_full_text
        }

        model_kwargs = {k:v for k, v in model_kwargs.items() if v is not None}

        super(LLamaModel, self).__init__(
            endpoint_name = endpoint_name,
            credentials_profile_name = credentials_profile,
            region_name="us-east-1",
            model_kwargs=model_kwargs,
            content_handler=content_handler,
            endpoint_kwargs={"CustomAttributes": 'accept_eula=true'})