from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db

# Імпортуємо функції безпеки та логування нашого модуля аудиту
from app.audit.logger import log_login_success, log_login_failed
from app.audit.detector import check_brute_force, check_off_hours_access

from pydantic import BaseModel

# Локальна Pydantic-модель запиту
class LoginRequest(BaseModel):
    username: str
    password: str

# Локальні функції-заглушки для тестування (щоб не падали імпорти)
class MockUser:
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

def authenticate_user(db: Session, username, password):
    # Тимчасова логіка для тестів: вхід успішний, лише якщо пароль "password123"
    if username == "admin" and password == "password123":
        return MockUser(user_id=1, username="admin", role="admin")
    return None

def create_access_token(data: dict):
    return "mocked_jwt_token_for_security_practice"


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    # Визначаємо IP-адресу клієнта
    ip = request.client.host if request.client else "unknown"

    # 1. ПЕРЕВІРКА BRUTE FORCE АТАКИ (Виконується першою для захисту додатка)
    if check_brute_force(db, ip):
        log_login_failed(db, credentials.username, ip, "brute_force_blocked")
        raise HTTPException(
            status_code=429,
            detail="Забагато невдалих спроб. Спробуйте пізніше."
        )

    # 2. АВТЕНТИФІКАЦІЯ
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        log_login_failed(db, credentials.username, ip)
        raise HTTPException(
            status_code=401, 
            detail="Невірний логін або пароль"
        )

    # 3. ПЕРЕВІРКА НА АНОМАЛЬНИЙ ЧАС ДОСТУПУ (Off-hours Access)
    check_off_hours_access(
        db, 
        user.id, 
        user.username, 
        ip, 
        datetime.now(timezone.utc).hour
    )
    
    # 4. ЛОГУВАННЯ УСПІШНОГО ВХОДУ В СИСТЕМУ
    log_login_success(db, user.id, user.username, ip)

    # 5. ГЕНЕРАЦІЯ JWT-ТОКЕНА
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }