from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType
from uuid import UUID


UserId = NewType('UserId', UUID)


class UserEnv(Enum):
    PROD = 'prod'
    PREPROD = 'preprod'
    STAGE = 'stage'


class UserDomain(Enum):
    CANARY = 'canary'
    REGULAR = 'regular'


@dataclass
class User:
    id: UserId = field(init=False)
    login: str
    password: str
    project_id: UUID
    env: UserEnv
    domain: UserDomain
    locktime: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)
