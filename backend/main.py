from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import json

import models, schemas, crud
from physics_engine import executor, evaluator

# Database configuration
class Settings(BaseSettings):
    database_url: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/problems/", response_model=schemas.Problem)
def create_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db)):
    # Validate test_cases is a valid JSON object
    if not isinstance(problem.test_cases, (dict, list)):
        try:
            json.loads(problem.test_cases)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Test cases must be a valid JSON object or array.")

    db_problem = crud.create_problem(db=db, problem=problem)
    return db_problem

@app.post("/api/solve_problem/")
async def solve_problem(user_code: str, problem_id: int, db: Session = Depends(get_db)):
    # TODO: Implement crud.get_problem(db, problem_id) to retrieve problem details
    # For now, using a dummy problem for demonstration
    dummy_problem = models.Problem(
        id=problem_id,
        title="Dummy Problem",
        description="Solve for x in x + 1 = 2",
        test_cases=json.dumps([
            {"input": "", "expected_output": "1"}
        ])
    )
    # In a real scenario, you'd fetch the problem from the DB:
    # problem = crud.get_problem(db, problem_id)
    # if not problem:
    #     raise HTTPException(status_code=404, detail="Problem not found")

    test_cases = json.loads(dummy_problem.test_cases)
    results = []

    for test_case in test_cases:
        test_input = test_case.get("input", "")
        expected_output = test_case.get("expected_output", "")

        execution_output = executor.execute_user_code(user_code, test_input)
        evaluation_result = evaluator.evaluate_solution(execution_output, expected_output)
        results.append({
            "test_input": test_input,
            "expected_output": expected_output,
            "execution_output": execution_output,
            "evaluation_result": evaluation_result
        })
    return {"problem_id": problem_id, "results": results}

