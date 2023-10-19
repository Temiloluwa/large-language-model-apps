"""
LLama Chat Model Loader from SageMaker Endpoint for Langchain

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

    2. Create an instance of LLamaChatModel with specific parameters
    llm = LLamaChatModel(
        endpoint_name="ep-llama-7b-chat",
        credentials_profile="my-aws-profile",
        max_new_tokens=256,
        top_p=0.8,
        temperature=0.5,
        return_full_text=False)

"""

import json
from typing import Dict, List
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


def process_prompt(input_string: str) -> List[Dict[str, str]]:
    """
    Convert a formatted string into a list of dictionaries.

    Args:
        input_string (str): The input string containing formatted content.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with roles and content.
    """

    def change_role_name(role_name: str) -> str:
        """Change the role name to llama2 format"""
        if role_name == "human":
            return "user"
        elif role_name == "ai":
            return "assistant"
        else:
            return role_name

    if "Human" in input_string or "Ai" in input_string or "System" in input_string:
        split_lines = [line.strip() for line in input_string.split('\n')]
        split_lines = [line.split(': ', 1) for line in split_lines]
        result = [{"role": change_role_name(role.lower()), "content": content} for role, content in split_lines]
    else:
        result = [{"role": "system", "content": "You are a helpful Assistant"}, {"role": "user", "content": input_string}]
    
    return result


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        payload = {
            "inputs": [process_prompt(prompt)],
            "parameters": model_kwargs
        }
        input_str = json.dumps(payload)
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generation"]["content"]


class LLamaChatModel(SagemakerEndpoint):
    def __init__(self,
        endpoint_name: str = None,
        credentials_profile: str = None,
        max_new_tokens: int = 128,
        temperature: float = 0.5,
        top_k: int = 10,
        top_p: float =  0.95,
        return_full_text: bool = False,
        content_handler: ContentHandler = ContentHandler()):

        model_kwargs = {
            "max_new_tokens": max_new_tokens,
            "return_full_text": return_full_text,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }

        super(LLamaChatModel, self).__init__(
            endpoint_name = endpoint_name,
            credentials_profile_name = credentials_profile,
            region_name="us-east-1",
            model_kwargs=model_kwargs,
            content_handler=content_handler,
            endpoint_kwargs={"CustomAttributes": 'accept_eula=true'})
