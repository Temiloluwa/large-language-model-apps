import os
import asyncio
from openai import OpenAI, AsyncOpenAI
from queryverse.llm import LLM

class OpenAILLM(LLM):

    def __init__(self, is_async=True):
        super(OpenAILLM, self).__init__()
        self.is_async = is_async
        self.client = self.create_client(self.is_async)
        

    def create_client(self, is_async=True):
        """ Creates a new OpenAI client

        Args:
            is_async (bool, optional): Async client if True. Defaults to True.

        Returns:
            client: OpenAI client
        """
        api_key = os.environ.get('OPENAI_API_KEY', '')
        if is_async:
            client = AsyncOpenAI(api_key=api_key)
        else:
            client = OpenAI(api_key=api_key)
        
        return client    


    def prompt(self,
               messages: list,
               temperature: float | int,
               max_tokens=3900,
               top_p: int = 1,
               stream: bool = True,
               model: str = 'gpt-3.5-turbo'):
        """Prompt the OpenAI model.

        Args:
            messages (list): List of message objects.
            temperature (float | int): Temperature for randomness in generating responses.
            max_tokens (int): Maximum number of tokens in the response (default is 3900).
            top_p (int): Value controlling the diversity of responses (default is 1).
            stream (bool): Whether to use stream-based responses (default is True).
            model (str): Name of the model to use (default is 'gpt-3.5-turbo').

        Returns:
            dict: Parsed response from the OpenAI model.
        """

        if self.is_async:
            raise ValueError("You cannot make call this method with an async client, set is_async=False")

        response = self.client.chat.completions.create(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            model=model,
            stream=stream)
        

        response = self.response_parser_chunked(response) if stream else \
                 self.response_parser(response)
        
        return response


    async def aprompt(self,
               messages: list,
               temperature: float | int,
               max_tokens=3900,
               top_p: int = 1,
               stream: bool = True,
               model: str = 'gpt-3.5-turbo'):
        """Async method to prompt the OpenAI model.

        Args:
            messages (list): List of message objects.
            temperature (float | int): Temperature for randomness in generating responses.
            max_tokens (int): Maximum number of tokens in the response (default is 3900).
            top_p (int): Value controlling the diversity of responses (default is 1).
            stream (bool): Whether to use stream-based responses (default is True).
            model (str): Name of the model to use (default is 'gpt-3.5-turbo').

        Returns:
            dict: Parsed response from the OpenAI model.
        """

        if not self.is_async:
            raise ValueError("You must use an async client, set is_async=True")

        response = await self.client.chat.completions.create(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            model=model,
            stream=stream)

        response = self.aresponse_parser_chunked(response) if stream else \
                 self.response_parser(response)
        
        return response


    def response_parser(self, response):
        """Parse the response from OpenAI.

        Args:
            response (dict): Response from OpenAI.

        Returns:
            dict: Parsed response including messages and usage information.
        """
        messages = []
        for choice in response.choices:
            messages.append({
                choice.message.role: choice.message.content,
                "finish_reason": choice.finish_reason,
            })

        response = {
            "messages": messages,
            "usage": dict(response.usage)
        }

        return response


    def response_parser_chunked(self, response):
        """Parse a chunked response from OpenAI.

        Args:
            response (dict): Chunked response from OpenAI.

        Yields:
            list: Parsed message objects from the response.
        """
        for chunk in response:
            chunk_message = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason or ""
            role = chunk_message.role or "no_role"
            content = chunk_message.content or ""
            yield { role: content, "finish_reason": finish_reason}


    async def aresponse_parser_chunked(self, response):
        """Async Parse a chunked response from OpenAI.

        Args:
            response (dict): Chunked response from OpenAI.

        Yields:
            list: Parsed message objects from the response.
        """
        async for chunk in response:
            chunk_message = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason or ""
            role = chunk_message.role or "no_role"
            content = chunk_message.content or ""
            yield { role: content, "finish_reason": finish_reason}