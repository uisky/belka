from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.types import DECIMAL
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import *
