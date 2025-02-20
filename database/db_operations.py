from sqlalchemy.orm import Session
import os

if "RENDER" in os.environ:
    from backend.database.db_models import Users_info
else:
    from database.db_models import Users_info


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
