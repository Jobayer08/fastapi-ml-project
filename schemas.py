from pydantic import BaseModel

class UserCreate(BaseModel):

    username: str

    password: str


class StudentInput(BaseModel):

    study_hours: float

    attendance: float

    previous_score: float