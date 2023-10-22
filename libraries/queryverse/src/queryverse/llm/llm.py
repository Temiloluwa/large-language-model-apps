from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def prompt(cls):
        pass


    @abstractmethod
    def response_parser(cls):
        pass

    
    @abstractmethod
    def response_parser_chunked(cls):
        pass
