from sqlmodel import Session, select
from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy import text
from typing import Optional, Annotated
from auth.schema_validation import StudentCreate, CollegesRead
from auth.schema import Colleges, Students
from auth.token import TokenOperation

# Custom import
from database.db_connection import get_db

router = APIRouter(tags=["College"])


def _prepare_college_data(load):
    fields = ("ID", "NAME", "SCRORE", "CITY", "STATE")
    return dict(zip(fields, load))


@router.get("/colleges")
def get_config(user: Annotated[str, Depends(TokenOperation._verify_token)], city_id: Optional[str] = Query(None),  db: Session = Depends(get_db)):
    extra_query = ""
    if city_id:
        extra_query = f"WHERE c.city_id = {city_id}"
    query = text("""
        SELECT 
            c.id AS ID, 
            c.name AS NAME, 
            c.score AS SCORE, 
            ci.name AS CITY, 
            s.name AS STATE
        FROM Colleges c
        JOIN Cities ci ON c.city_id = ci.id
        JOIN States s ON c.state_id = s.id
        %s
    """ % (extra_query))
    result = db.exec(query).all()

    return list(map(_prepare_college_data, result))


@router.get("/college/{college_id}", response_model=CollegesRead)
def get_college_by_id(token: Annotated[str, Depends(TokenOperation._verify_token)], college_id: int, db: Session = Depends(get_db)):
    """Fetch a college record by its ID"""
    college = db.exec(select(Colleges).where(
        Colleges.id == college_id)).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college


@router.post("/add/student")
def add_student(token: Annotated[str, Depends(TokenOperation._verify_token)], student_data: StudentCreate, db: Session = Depends(get_db)):
    """Fetch a college record by its ID"""
    student = db.exec(select(Students).where(
        Students.enroll_num == student_data.enroll_num)).first()
    if student:
        raise HTTPException(
            status_code=403, detail="Student already exists with this Enroll Number")
    else:
        # Step 1: Get the college details using college_code
        college = db.exec(select(Colleges).where(
            Colleges.college_code == student_data.college_code)).first()

        if not college:
            raise HTTPException(
                status_code=404, detail="College not found with the given code")

        # Step 2: Extract IDs
        # Step 2: Create Student with auto-updated fields
        new_student = Students(
            name=student_data.name,
            enroll_num=student_data.enroll_num,
            college_id=college.id,   # ✅ Auto-fetched
            city_id=college.city_id,  # ✅ Auto-fetched
            state_id=college.state_id  # ✅ Auto-fetched
        )

        # Step 3: Create new student record
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return {"message": "Student created successfully", "student_id": new_student.id}
