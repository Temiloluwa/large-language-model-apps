"""
LLama Model Loader from SageMaker Endpoint for Langchain

This module provides functions to load a LLama model deployed on Amazon SageMaker.
It allows users to retrieve inference endpoints and perform predictions using the model.

Author: Temiloluwa Adeoti
License: MIT License
Date: August 19, 2023

Required Libraries:
    - boto3 (Amazon Web Services SDK)
    - langchain (LLama's Language Model SDK)

Usage:
    1. Install the required libraries:
    
    >>> pip install boto3 langchain

    2. Create an instance of LLamaModel with specific parameters
    llm = LLamaModel(
        endpoint_name="ep-llama-7b",
        credentials_profile="temmie",
        max_new_tokens=256,
        top_p=0.8,
        temperature=0.5,
        return_full_text=False)
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

        super(LLamaModel, self).__init__(
            endpoint_name = endpoint_name,
            credentials_profile_name = credentials_profile,
            region_name="us-east-1",
            model_kwargs=model_kwargs,
            content_handler=content_handler,
            endpoint_kwargs={"CustomAttributes": 'accept_eula=true'})