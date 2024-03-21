from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    children = relationship("Child")  # Definición de la relación con la clase Child

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parents.id'))  # Definición de la clave foránea

# En este ejemplo, estamos definiendo una relación uno a muchos entre las clases Parent y Child.
# Cada instancia de la clase Parent puede tener múltiples instancias de la clase Child asociadas a ella.
# La relación se define en la clase Parent usando la instrucción relationship.
# SQLAlchemy usa la clave foránea definida en la clase Child para establecer la relación.
