from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def prompt(self):
        pass


    @abstractmethod
    def load_api_key(self):
        pass

    @abstractmethod
    def create_llm(self):
        pass


    @abstractmethod
    def response_parser(self):
        pass
