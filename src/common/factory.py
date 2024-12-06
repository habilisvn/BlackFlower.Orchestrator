from dataclasses import dataclass
from typing import TypeVar, Type
from pydantic import BaseModel
from mongoengine import Document

T = TypeVar('T', bound=Document)
M = TypeVar('M', bound=BaseModel)

class DocumentFactory:
    @staticmethod
    def create_document(model: M, document_class: Type[T]) -> T:
        """
        Creates a document instance from a pydantic model
        
        Args:
            model: Pydantic model instance containing the data
            document_class: Document class to instantiate
            
        Returns:
            Document instance populated with model data
        """
        # Convert pydantic model to dict and create document
        model_data = model.model_dump()
        return document_class(**model_data)


@dataclass
class Banana:
    name: str
    color: str


@dataclass
class Apple:
    name: str
    color: str


class Box[T]:
    def __init__(self) -> None:
        self.items: list[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get(self) -> T:
        return self.items.pop()



box = Box[Banana]()
box.add(Banana(name="Banana", color="Yellow"))
box.add(Apple(name="Apple", color="Red"))

print(box.get())