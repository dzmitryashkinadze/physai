from sqlalchemy import create_engine, Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

from sqlalchemy.types import JSON
import uuid

DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    summary = Column(Text)
    logo_url = Column(String)
    topic = Column(String)
    difficulty = Column(String)

    problems = relationship("Problem", back_populates="course")

class Problem(Base):
    __tablename__ = "problems"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(Text)
    solution_markdown = Column(Text)
    solution_equation = Column(Text)
    known_parameters = Column(JSON) # For SQLite, this will store JSON as TEXT
    variable_to_find = Column(String)
    difficulty = Column(String)
    figures = Column(JSON) # For SQLite, this will store JSON as TEXT
    order = Column(Integer)
    course_id = Column(String(36), ForeignKey("courses.id"))

    course = relationship("Course", back_populates="problems")
    problem_topics = relationship("ProblemTopic", back_populates="problem")
    problem_physics_laws = relationship("ProblemPhysicsLaw", back_populates="problem")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)

    problem_topics = relationship("ProblemTopic", back_populates="topic")

class PhysicsLaw(Base):
    __tablename__ = "physics_laws"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    equation = Column(Text)

    problem_physics_laws = relationship("ProblemPhysicsLaw", back_populates="physics_law")

# Junction Tables
class ProblemTopic(Base):
    __tablename__ = "problem_topics"
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    topic_id = Column(String(36), ForeignKey("topics.id"), primary_key=True)

    problem = relationship("Problem", back_populates="problem_topics")
    topic = relationship("Topic", back_populates="problem_topics")

class ProblemPhysicsLaw(Base):
    __tablename__ = "problem_physics_laws"
    problem_id = Column(String(36), ForeignKey("problems.id"), primary_key=True)
    physics_law_id = Column(String(36), ForeignKey("physics_laws.id"), primary_key=True)

    problem = relationship("Problem", back_populates="problem_physics_laws")
    physics_law = relationship("PhysicsLaw", back_populates="problem_physics_laws")

def create_db_tables():
    Base.metadata.create_all(bind=engine)
