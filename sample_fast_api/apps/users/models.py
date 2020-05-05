import uuid

from sqlalchemy.dialects.postgresql import ARRAY, UUID

from sample_fast_api.main import db


class Address(db.Model):
    __tablename__ = "users_address"

    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    city = db.Column(db.String(32), nullable=False)
    complement = db.Column(db.String(128))
    country = db.Column(db.String(64), nullable=False)
    number = db.Column(db.String(16), nullable=False)
    postal_code = db.Column(db.String(8), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    street = db.Column(db.String(128), nullable=False)


class User(db.Model):
    __tablename__ = "users_user"

    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    address_id = db.Column(UUID(), db.ForeignKey("users_address.id"))
    email = db.Column(db.String(255), nullable=False, index=True)
    is_active = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    password = db.Column(db.String(248), nullable=False)
    permissions = db.Column(ARRAY(db.String), nullable=False)
