from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType
from uuid import UUID


UserId = NewType('UserId', UUID)


@dataclass(slots=True)
class User:
    id: UserId = field(init=False)
    login: str
    password: str
    project_id: UUID
    env: str
    domain: str
    locktime: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)
