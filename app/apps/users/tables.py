import uuid

from sqlalchemy import Boolean, Column, ForeignKey, MetaData, String, Table
from sqlalchemy.dialects.postgresql import ARRAY, UUID

metadata = MetaData()

address = Table(
    "users_address",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("city", String(32), nullable=False),
    Column("complement", String(128), nullable=True),
    Column("country", String(64), nullable=False),
    Column("number", String(16), nullable=False),
    Column("postal_code", String(8), nullable=False),
    Column("state", String(2), nullable=False),
    Column("street", String(128), nullable=False),
)


user = Table(
    "users_user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("address_id", UUID(as_uuid=True), ForeignKey("users_address.id"), nullable=False),
    Column("email", String(255), index=True, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("name", String(64), index=True, nullable=False),
    Column("password", String(248), nullable=False),
    Column("permissions", ARRAY(String), nullable=False),
)
