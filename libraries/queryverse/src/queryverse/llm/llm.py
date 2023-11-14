from abc import ABC, abstractmethod

class LLM(ABC):
    
    @abstractmethod
    def prompt(self):
        pass

    @abstractmethod
    async def aprompt(self):
        pass

