from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User  # Suponiendo que tienes definido el modelo User en un archivo models.py

# Crear una sesión para interactuar con la base de datos
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

def create_user(username, email, password):
    """Crear un nuevo usuario"""
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
    return user

def get_user_by_id(user_id):
    """Obtener un usuario por su ID"""
    return session.query(User).filter_by(id=user_id).first()

def get_user_by_username(username):
    """Obtener un usuario por su nombre de usuario"""
    return session.query(User).filter_by(username=username).first()

def update_user_password(user_id, new_password):
    """Actualizar la contraseña de un usuario"""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.password = new_password
        session.commit()
        return True
    return False

def delete_user(user_id):
    """Eliminar un usuario por su ID"""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False
