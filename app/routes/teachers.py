from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Grade
from app.auth.dependencies import require_role

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/grades")
def get_all_grades(
    user: User = Depends(require_role("teacher", "admin")),
    db: Session = Depends(get_db),
):
    grades = db.query(Grade).all()

    return {
        "count": len(grades),
        "grades": [
            {
                "student_id": g.student_id,
                "subject_id": g.subject_id,
                "value": g.value,
                "date": str(g.date),
            }
            for g in grades
        ],
    }