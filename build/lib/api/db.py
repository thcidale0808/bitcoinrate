"""
sharedmodels provides native sqlalchemy models. This file wraps the models
via flask-sqlalchemy, which provides automatic session handling 
within a request context, but the sharedmodels may be used outside
of flask directly by other components.

"""

from flask_sqlalchemy import SQLAlchemy

from sharedmodels.db import get_session_scope
from sharedmodels.models import Base

db = SQLAlchemy(metadata=Base.metadata)
