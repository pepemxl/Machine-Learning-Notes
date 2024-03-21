from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Tabla para representar los servicios
class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship("Owner", back_populates="services")
    endpoints = relationship("Endpoint", back_populates="service")
    files = relationship("File", back_populates="service")

# Tabla para representar los endpoints
class Endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship("Owner", back_populates="endpoints")
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Service", back_populates="endpoints")

# Tabla para representar los archivos
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Service", back_populates="files")
    attributes = relationship("Attribute", back_populates="file")

# Tabla para representar los atributos de los archivos
class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship("File", back_populates="attributes")

# Tabla para representar los propietarios (owners)
class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    services = relationship("Service", back_populates="owner")
    endpoints = relationship("Endpoint", back_populates="owner")

# Crear una base de datos SQLite en memoria
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar datos al knowledge graph
owner1 = Owner(name='Company A')
owner2 = Owner(name='Company B')

service1 = Service(name='Service 1', owner=owner1)
service2 = Service(name='Service 2', owner=owner2)

endpoint1 = Endpoint(name='Endpoint 1', owner=owner1, service=service1)
endpoint2 = Endpoint(name='Endpoint 2', owner=owner2, service=service2)

file1 = File(name='file1.py', path='/path/to/file1.py', service=service1)
file2 = File(name='file2.py', path='/path/to/file2.py', service=service1)
file3 = File(name='file3.py', path='/path/to/file3.py', service=service2)

attribute1 = Attribute(key='author', value='John Doe', file=file1)
attribute2 = Attribute(key='date_created', value='2023-01-01', file=file1)

session.add_all([owner1, owner2, service1, service2, endpoint1, endpoint2, file1, file2, file3, attribute1, attribute2])
session.commit()

# Consultar la base de datos para verificar los datos almacenados
owners = session.query(Owner).all()
services = session.query(Service).all()
endpoints = session.query(Endpoint).all()
files = session.query(File).all()
attributes = session.query(Attribute).all()

print("Owners:")
for owner in owners:
    print(f"ID: {owner.id}, Name: {owner.name}")

print("\nServices:")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Owner: {service.owner.name}")

print("\nEndpoints:")
for endpoint in endpoints:
    print(f"ID: {endpoint.id}, Name: {endpoint.name}, Owner: {endpoint.owner.name}, Service: {endpoint.service.name}")

print("\nFiles:")
for file in files:
    print(f"ID: {file.id}, Name: {file.name}, Path: {file.path}, Service: {file.service.name}")

print("\nAttributes:")
for attribute in attributes:
    print(f"ID: {attribute.id}, Key: {attribute.key}, Value: {attribute.value}, File: {attribute.file.name}")

