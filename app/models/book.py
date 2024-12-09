from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    quantity: int
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        return cls(
            id=data.get('id', 0),
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
