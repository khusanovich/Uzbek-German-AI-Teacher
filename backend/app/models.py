"""
SQLAlchemy models for curriculum and learner progress.
"""
from sqlalchemy import Column, String, Text, JSON, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Unit(Base):
    """Curriculum unit."""
    __tablename__ = "units"

    id = Column(String, primary_key=True)
    level = Column(String, nullable=False, index=True)  # A1.1, A1.2, etc.
    title = Column(String, nullable=False)
    objectives = Column(JSON, nullable=False)  # list of strings
    target_vocab = Column(JSON, nullable=False, default=list)  # list of strings


class LearnerProgress(Base):
    """Track learner's progress through the curriculum."""
    __tablename__ = "learner_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(String, nullable=False, index=True)  # for multi-user support later
    level = Column(String, nullable=False)
    completed_unit_ids = Column(JSON, nullable=False, default=list)  # list of completed unit IDs
    mistakes_log = Column(JSON, nullable=False, default=list)  # [{unit_id, mistake, timestamp}, ...]
    current_unit_id = Column(String, nullable=True)  # currently active unit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
