from sqlalchemy import create_engine, Column, String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
import uuid
import json

# Database setup
DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Models based on DATA_MODEL.md
class Course(Base):
    __tablename__ = "courses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    summary = Column(Text)
    logo_url = Column(String)
    topic = Column(String)
    difficulty = Column(String)

    problems = relationship("Problem", back_populates="course")

class Problem(Base):
    __tablename__ = "problems"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(Text)
    solution_markdown = Column(Text)
    solution_equation = Column(Text)
    known_parameters = Column(JSON) # For SQLite, this will store JSON as TEXT
    variable_to_find = Column(String)
    difficulty = Column(String)
    figures = Column(JSON) # For SQLite, this will store JSON as TEXT
    order = Column(Integer)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))

    course = relationship("Course", back_populates="problems")
    problem_topics = relationship("ProblemTopic", back_populates="problem")
    problem_physics_laws = relationship("ProblemPhysicsLaw", back_populates="problem")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)

    problem_topics = relationship("ProblemTopic", back_populates="topic")

class PhysicsLaw(Base):
    __tablename__ = "physics_laws"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    equation = Column(Text)

    problem_physics_laws = relationship("ProblemPhysicsLaw", back_populates="physics_law")

# Junction Tables
class ProblemTopic(Base):
    __tablename__ = "problem_topics"
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), primary_key=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), primary_key=True)

    problem = relationship("Problem", back_populates="problem_topics")
    topic = relationship("Topic", back_populates="problem_topics")

class ProblemPhysicsLaw(Base):
    __tablename__ = "problem_physics_laws"
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), primary_key=True)
    physics_law_id = Column(UUID(as_uuid=True), ForeignKey("physics_laws.id"), primary_key=True)

    problem = relationship("Problem", back_populates="problem_physics_laws")
    physics_law = relationship("PhysicsLaw", back_populates="problem_physics_laws")

def create_tables():
    Base.metadata.create_all(bind=engine)

def generate_synthetic_data():
    db = SessionLocal()
    try:
        # Create Topics
        kinematics_topic = Topic(name="Kinematics")
        electrostatics_topic = Topic(name="Electrostatics")
        thermodynamics_topic = Topic(name="Thermodynamics")
        db.add_all([kinematics_topic, electrostatics_topic, thermodynamics_topic])
        db.commit()
        db.refresh(kinematics_topic)
        db.refresh(electrostatics_topic)
        db.refresh(thermodynamics_topic)

        # Create Physics Laws
        newtons_second_law = PhysicsLaw(name="Newton's Second Law", equation="F = ma")
        ohms_law = PhysicsLaw(name="Ohm's Law", equation="V = IR")
        conservation_of_energy = PhysicsLaw(name="Conservation of Energy", equation="E_initial = E_final")
        db.add_all([newtons_second_law, ohms_law, conservation_of_energy])
        db.commit()
        db.refresh(newtons_second_law)
        db.refresh(ohms_law)
        db.refresh(conservation_of_energy)

        # Create Courses
        course1 = Course(
            title="Introduction to Mechanics",
            summary="A foundational course covering classical mechanics.",
            logo_url="/static/mechanics_logo.png",
            topic="Mechanics",
            difficulty="Beginner"
        )
        course2 = Course(
            title="Electromagnetism Fundamentals",
            summary="Explore the basics of electric and magnetic fields.",
            logo_url="/static/em_logo.png",
            topic="Electromagnetism",
            difficulty="Intermediate"
        )
        db.add_all([course1, course2])
        db.commit()
        db.refresh(course1)
        db.refresh(course2)

        # Create Problems
        problem1 = Problem(
            title="Kinematics Problem 1",
            description="A car accelerates from rest...",
            solution_markdown="Solution details for kinematics problem 1.",
            solution_equation="v = u + at",
            known_parameters=json.dumps({"u": {"unit": "m/s"}, "a": {"unit": "m/s^2"}, "t": {"unit": "s"}}),
            variable_to_find="v",
            difficulty="School Grade",
            figures=json.dumps(["/static/kinematics_fig1.png"]),
            order=1,
            course=course1
        )
        problem2 = Problem(
            title="Electrostatics Problem 1",
            description="Two point charges are placed...",
            solution_markdown="Solution details for electrostatics problem 1.",
            solution_equation="F = k * q1 * q2 / r^2",
            known_parameters=json.dumps({"k": {"unit": "N m^2/C^2"}, "q1": {"unit": "C"}, "q2": {"unit": "C"}, "r": {"unit": "m"}}),
            variable_to_find="F",
            difficulty="University",
            figures=json.dumps(["/static/electrostatics_fig1.png", "/static/electrostatics_fig2.png"]),
            order=1,
            course=course2
        )
        problem3 = Problem(
            title="Kinematics Problem 2",
            description="A ball is thrown vertically upwards...",
            solution_markdown="Solution details for kinematics problem 2.",
            solution_equation="h = ut + 0.5gt^2",
            known_parameters=json.dumps({"u": {"unit": "m/s"}, "g": {"unit": "m/s^2"}, "t": {"unit": "s"}}),
            variable_to_find="h",
            difficulty="School Grade",
            figures=json.dumps([]),
            order=2,
            course=course1
        )
        db.add_all([problem1, problem2, problem3])
        db.commit()
        db.refresh(problem1)
        db.refresh(problem2)
        db.refresh(problem3)

        # Link Problems to Topics
        db.add_all([
            ProblemTopic(problem=problem1, topic=kinematics_topic),
            ProblemTopic(problem=problem3, topic=kinematics_topic),
            ProblemTopic(problem=problem2, topic=electrostatics_topic)
        ])
        db.commit()

        # Link Problems to Physics Laws
        db.add_all([
            ProblemPhysicsLaw(problem=problem1, physics_law=newtons_second_law),
            ProblemPhysicsLaw(problem=problem3, physics_law=newtons_second_law),
            ProblemPhysicsLaw(problem=problem2, physics_law=ohms_law)
        ])
        db.commit()

        print("Synthetic data generated successfully!")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    generate_synthetic_data()
