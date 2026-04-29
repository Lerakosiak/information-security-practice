from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.dependencies import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
def get_all_users(
    user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    users = db.query(User).all()

    return {
        "count": len(users),
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_active": u.is_active,
            }
            for u in users
        ],
    }