import os
import shutil
from datetime import datetime
from app.crypto.encryption import get_fernet

def create_encrypted_backup():
    # Автоматично знаходимо корінь проекту відносно папки scripts/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Формуємо шляхи динамічно
    db_path = os.path.join(base_dir, "data", "app.db")
    backup_dir = os.path.join(base_dir, "backups")
    
    # Створюємо папку для бекапів, якщо її немає
    os.makedirs(backup_dir, exist_ok=True)
    
    # Генеруємо ім'я файлу з міткою часу
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_backup_path = f"{db_path}.{timestamp}.bak"
    final_encrypted_path = os.path.join(backup_dir, f"dekanat_backup_{timestamp}.db.enc")
    
    print("Старт створення резервної копії бази даних...")
    print(f"Шукаємо базу за шляхом: {db_path}")
    
    try:
        # 1. Перевіряємо наявність оригінального файлу бази
        if not os.path.exists(db_path):
            # Якщо файл не знайшовся в корені, спробуємо перевірити в папці data/
            db_path = os.path.join(base_dir, "data", "dekanat.db")
            print(f"Спроба знайти базу в підпапці: {db_path}")
            if not os.path.exists(db_path):
                print("Критична помилка: Файл бази даних dekanat.db ніде не знайдено!")
                return
            
        # 2. Створюємо тимчасову копію
        shutil.copy2(db_path, temp_backup_path)
        
        # 3. Зчитуємо бінарні дані
        with open(temp_backup_path, "rb") as f:
            db_data = f.read()
            
        # 4. Шифруємо весь файл
        fernet = get_fernet()
        encrypted_data = fernet.encrypt(db_data)
        
        # 5. Записуємо зашифровані дані
        with open(final_encrypted_path, "wb") as f:
            f.write(encrypted_data)
            
        print(f"Успішно створено ЗАШИФРОВАНИЙ бекап: {final_encrypted_path}")
        
    except Exception as e:
        print(f"Критична помилка під час створення бекапу: {e}")
        
    finally:
        # 6. Очищаємо незашифровані сліди
        if os.path.exists(temp_backup_path):
            os.remove(temp_backup_path)
            print("Тимчасові незашифровані файли успішно очищено.")

if __name__ == "__main__":
    create_encrypted_backup()