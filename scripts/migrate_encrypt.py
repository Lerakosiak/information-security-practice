from sqlalchemy import text
from app.database import SessionLocal
from app.models import User
from app.crypto.encryption import encrypt_field

def migrate_existing_data():
    db = SessionLocal()
    try:
        # Отримуємо всіх користувачів із бази
        users = db.query(User).all()
        migrated_count = 0

        print("Старт міграції та шифрування даних користувачів...")
        
        for user in users:
            # Перевіряємо, чи дані вже зашифровані (шифрований Fernet-рядок завжди починається з gAAAAA)
            if user._email and not user._email.startswith("gAAAAA"):
                raw_email = user._email
                # Зашифровуємо відкритий email
                user._email = encrypt_field(raw_email)
                migrated_count += 1
                print(f"Користувача [{user.username}] успішно зашифровано.")

        if migrated_count > 0:
            db.commit()
            print(f"Міграція успішно завершена! Зашифровано користувачів: {migrated_count}")
        else:
            print("Усі записи вже зашифровані або база даних порожня. Міграція не потрібна.")

    except Exception as e:
        db.rollback()
        print(f"Помилка під час міграції: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_existing_data()