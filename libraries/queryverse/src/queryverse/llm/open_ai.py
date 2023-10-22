import openai
from queryverse.llm import LLM

class OpenAI(LLM):
    @classmethod
    def prompt(cls,
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

        response = openai.ChatCompletion.create(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            model=model,
            stream=stream)

        response = cls.response_parser_chunked(response) if stream else \
                 cls.response_parser(response)
        
        return response

    @classmethod
    def response_parser(cls, response):
        """Parse the response from OpenAI.

        Args:
            response (dict): Response from OpenAI.

        Returns:
            dict: Parsed response including messages and usage information.
        """

        messages = []
        usage = response.get("usage")
        usage = usage.to_dict() if hasattr(usage, 'to_dict') else usage
        for choice in response.get("choices"):
            messages.append({
                choice["message"]["role"]: choice["message"]["content"],
                "finish_reason": choice.get("finish_reason"),
            })

        response = {
            "messages": messages,
            "usage": usage
        }

        return response


    @classmethod
    def response_parser_chunked(cls, response):
        """Parse a chunked response from OpenAI.

        Args:
            response (dict): Chunked response from OpenAI.

        Yields:
            list: Parsed message objects from the response.
        """

        for chunk in response:
            chunk_message = chunk.get('choices')[0].get('delta')
            yield {
                chunk_message.get("role", "no_role"): chunk_message.get("content", ""),
                "finish_reason": chunk.get('choices')[0].get('finish_reason')
            }
