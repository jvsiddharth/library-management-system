from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

@dataclass
class Book:
    id: int
    title: str
    author: str
    isbn: str
    quantity: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        return cls(
            id=data.get('id'),
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            quantity=data['quantity'],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# In-memory storage
books: Dict[int, Book] = {}
