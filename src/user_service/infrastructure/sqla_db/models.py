from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Integer,
    UUID,
    Enum,
    String,
    Column,
    MetaData,
    Table,
    DateTime,
)
from sqlalchemy.orm import registry

from user_service.application.models.user import User, UserDomain, UserEnv

metadata_obj = MetaData()
mapper_registry = registry()

user = Table(
    'user',
    metadata_obj,
    Column('id', UUID, primary_key=True, default=uuid4),
    Column('login', String, nullable=False),
    Column('password', String, nullable=False),
    Column('project_id', UUID, nullable=False),
    Column(
        'env',
        Enum(UserEnv, values_callable=lambda enum: [e.value for e in enum]),
        nullable=False,
    ),
    Column(
        'domain',
        Enum(UserDomain, values_callable=lambda enum: [e.value for e in enum]),
        nullable=False,
    ),
    Column('locktime', Integer, nullable=False, default=0),
    Column('created_at', DateTime, nullable=False, default=datetime.now),
)

mapper_registry.map_imperatively(User, user)
