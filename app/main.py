from fastapi import FastAPI
from app.database import Base, engine

# Імпортуємо нові компоненти аудиту безпеки
from app.audit.models import AuditLog
from app.audit.middleware import AuditMiddleware
from app.audit.router import router as audit_router

# Твої існуючі роутери додатку
from app.auth.router import router as auth_router
from app.routes.students import router as students_router
from app.routes.teachers import router as teachers_router
from app.routes.admin import router as admin_router

# Компоненти захисту та CORS
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limiter import limiter

app = FastAPI(
    title="Електронний деканат",
    description="API для управління академічними даними",
    version="0.5.0"
)

# Автоматичне створення таблиць (включаючи audit_log) при запуску для обходу багів Alembic
Base.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Черговість middleware важлива: спочатку загальна безпека, потім аудит запитів
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:3010",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

# Підключення роутерів
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(teachers_router)
app.include_router(admin_router)

# Реєструємо адмін-панель моніторингу подій безпеки
app.include_router(audit_router, prefix="/admin", tags=["audit"])

@app.get("/")
async def root():
    return {"message": "Електронний деканат API v0.5.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables)
    }