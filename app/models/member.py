from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

@dataclass
class Member:
    id: int
    name: str
    email: str
    password_hash: str
    books_borrowed: List[int]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: Dict) -> 'Member':
        return cls(
            id=data.get('id'),
            name=data['name'],
            email=data['email'],
            password_hash=cls.hash_password(data['password']),
            books_borrowed=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'books_borrowed': self.books_borrowed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)

# In-memory storage
members: Dict[int, Member] = {}
