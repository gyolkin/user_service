from uuid import uuid4
from datetime import datetime

from sqlalchemy import Integer, UUID, String, Column, MetaData, Table, DateTime
from sqlalchemy.orm import registry

from user_service.application.models import User

metadata_obj = MetaData()
mapper_registry = registry()

user = Table(
    'user',
    metadata_obj,
    Column('id', UUID, primary_key=True, default=uuid4),
    Column('login', String, nullable=False),
    Column('password', String, nullable=False),
    Column('project_id', UUID, nullable=False),
    Column('env', String, nullable=False),
    Column('domain', String, nullable=False),
    Column('locktime', Integer, nullable=False, default=0),
    Column('created_at', DateTime, nullable=False, default=datetime.now),
)

mapper_registry.map_imperatively(User, user)
