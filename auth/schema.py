from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, DECIMAL, func
)
from sqlalchemy.orm import relationship
from database.connection import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class Colleges(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    score = Column(Integer, index=True)
    city_id = Column(Integer, index=True)
    state_id = Column(Integer, index=True)
    college_code = Column(String, nullable=False, unique=True)

    students = relationship(
        "Students", back_populates="college", cascade="all, delete-orphan")
    placements = relationship("CollegePlacement", back_populates="college",
                              cascade="all, delete", passive_deletes=True)
    courses = relationship(
        "CollegeWiseCourse",
        back_populates="college",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    college_id = Column(Integer, ForeignKey(
        "colleges.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(Integer, index=True)
    state_id = Column(Integer, index=True)
    enroll_num = Column(String, index=True)

    college = relationship("Colleges", back_populates="students")


class CollegePlacement(Base):
    __tablename__ = "college_placement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey(
        "colleges.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    highest_placement = Column(DECIMAL(10, 2))
    average_placement = Column(DECIMAL(10, 2))
    median_placement = Column(DECIMAL(10, 2))
    placement_rate = Column(DECIMAL(5, 2))

    college = relationship("Colleges", back_populates="placements")


class CollegeWiseCourse(Base):
    __tablename__ = "college_wise_course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey(
        "colleges.id", ondelete="CASCADE"), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_duration = Column(Integer, nullable=False)
    course_fee = Column(DECIMAL(10, 2))

    # Optional relationship to Colleges model
    college = relationship("Colleges", back_populates="courses")

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)  # optional: enforce unique names


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)  # optional: enforce unique names