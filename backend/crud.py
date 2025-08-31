from sqlalchemy.orm import Session
import models, schemas
import json

def create_problem(db: Session, problem: schemas.ProblemCreate):
    db_problem = models.Problem(
        title=problem.title,
        description=problem.description,
        test_cases=json.dumps(problem.test_cases) # Store JSON as string
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem
