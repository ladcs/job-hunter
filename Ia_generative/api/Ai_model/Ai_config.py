from abc import ABC, abstractmethod

class Ai_Config(ABC):
    def __init__(self, prompt: str):
        self.prompt = prompt

    @property
    @abstractmethod
    def model(self) -> str: ...


    @property
    @abstractmethod
    def max_tokens(self) -> int: ...

    @property
    @abstractmethod
    def args(self) -> dict: ...

    @abstractmethod
    def client(self):
        raise NotImplementedError("Client method must be implemented by subclasses")
    
    @property
    def reasoning(self) -> str | None: ...

    @property
    def temperature(self) -> float | None: ...