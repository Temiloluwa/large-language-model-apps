import openai
import os
from queryverse.utils import ApiKeyNotFoundError, get_api_key
from queryverse.llm import LLM

class OpenAI(LLM):

    def __init__(self, 
            model_name="gpt-3.5-turbo",
            api_key=None,
            temperature=0):
        super(OpenAI, self).__init__()
        self._model_name = model_name
        self._temperature = temperature
        self.load_api_key(api_key)

        
    def load_api_key(self, api_key):
        """ load api key """
        try:
            openai.api_key = get_api_key(api_key)
        except ApiKeyNotFoundError as e:
            raise e

    def create_llm(self):
        pass


    def prompt(self, messages=None):
        """prompt a model """
        response = openai.ChatCompletion.create(
                                    model=self._model_name,
                                    temperature=self._temperature,
                                    messages=messages)
        response = self.response_parser(response)
        return response


    def response_parser(self, response):
        """Parser for response from OpenAI

        Args:
            response (_type_): _description_
        """
        if len(response.get("choices")) > 0:
            messages = [{choice["message"]["role"]: choice["message"]["content"]\
                 for choice in response.get("choices")}]
        #finish_reasons = [{"finish_reason": choice["finish_reason"] for choice in response.get("choices")}]
            return messages
        return "No Response"
