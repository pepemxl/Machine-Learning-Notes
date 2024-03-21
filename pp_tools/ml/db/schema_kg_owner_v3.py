from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Tabla para representar los proyectos
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager_id = Column(Integer, ForeignKey('managers.id'))
    manager = relationship("Manager", back_populates="projects")
    operators = relationship("Operator", back_populates="project")
    services = relationship("Service", back_populates="project")
    endpoints = relationship("Endpoint", back_populates="project")

# Tabla para representar los gerentes de proyecto
class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship("Project", back_populates="manager")

# Tabla para representar los operadores de proyecto
class Operator(Base):
    __tablename__ = 'operators'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="operators")

# Tabla para representar los servicios
class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="services")
    files = relationship("File", back_populates="service")

# Tabla para representar los endpoints
class Endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="endpoints")
    files = relationship("File", back_populates="endpoint")

# Tabla para representar los archivos
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Service", back_populates="files")
    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    endpoint = relationship("Endpoint", back_populates="files")
    attributes = relationship("Attribute", back_populates="file")

# Tabla para representar los atributos de los archivos
class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship("File", back_populates="attributes")

# Crear una base de datos SQLite en memoria
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar datos al knowledge graph
manager1 = Manager(name='Manager A')
operator1 = Operator(name='Operator 1')
operator2 = Operator(name='Operator 2')
project1 = Project(name='Project 1', manager=manager1, operators=[operator1, operator2])

service1 = Service(name='Service 1', project=project1)
endpoint1 = Endpoint(name='Endpoint 1', project=project1)

file1 = File(name='file1.py', path='/path/to/file1.py', service=service1)
file2 = File(name='file2.py', path='/path/to/file2.py', endpoint=endpoint1)

attribute1 = Attribute(key='author', value='John Doe', file=file1)
attribute2 = Attribute(key='date_created', value='2023-01-01', file=file1)

session.add_all([manager1, operator1, operator2, project1, service1, endpoint1, file1, file2, attribute1, attribute2])
session.commit()

# Consultar la base de datos para verificar los datos almacenados
managers = session.query(Manager).all()
operators = session.query(Operator).all()
projects = session.query(Project).all()
services = session.query(Service).all()
endpoints = session.query(Endpoint).all()
files = session.query(File).all()
attributes = session.query(Attribute).all()

print("Managers:")
for manager in managers:
    print(f"ID: {manager.id}, Name: {manager.name}")

print("\nOperators:")
for operator in operators:
    print(f"ID: {operator.id}, Name: {operator.name}, Project: {operator.project.name}")

print("\nProjects:")
for project in projects:
    print(f"ID: {project.id}, Name: {project.name}, Manager: {project.manager.name}")

print("\nServices:")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Project: {service.project.name}")



def third_party_owners():
    # Suponiendo que ya tienes los objetos cargados en la sesión de SQLAlchemy

    # Paso 1: Identificar las bibliotecas de terceros
    third_party_libraries = session.query(File).filter_by(is_third_party=True).all()

    # Paso 2: Obtener los propietarios de cada biblioteca de terceros
    owners_of_libraries = {}
    for library in third_party_libraries:
        owners_of_libraries[library] = library.owner

    # Paso 3: Identificar el gerente asociado con cada propietario
    managers_of_libraries = {}
    for library, owner in owners_of_libraries.items():
        project = session.query(Project).filter_by(owner=owner).first()
        managers_of_libraries[library] = project.manager

    # Ahora 'managers_of_libraries' contendrá un mapeo de cada biblioteca de terceros a su gerente asociado


def third_party_owners2():
    """
    1. Análisis de los imports: Escanea tus archivos de código Python para identificar los imports de bibliotecas externas. Puedes hacer esto mediante análisis estático del código o utilizando herramientas como ast en Python para analizar sintácticamente los archivos.
    2. Mapeo de imports a bibliotecas: A partir de los imports identificados, mapea cada import a la biblioteca de terceros correspondiente. Esto puede requerir un poco de análisis adicional para manejar imports con alias o imports de submódulos.
    3. Asociación de bibliotecas con propietarios y gerentes: Una vez que hayas identificado las bibliotecas de terceros a partir de los imports, puedes seguir el mismo proceso que antes para asociar estas bibliotecas con propietarios y gerentes en tu knowledge graph.
    """
    # Suponiendo que tienes el código Python almacenado en tu repositorio y los objetos ya cargados en la sesión de SQLAlchemy

    # Paso 1: Escaneo de los archivos para identificar imports de bibliotecas externas
    external_libraries = set()
    for file in session.query(File).all():
        with open(file.path, 'r') as f:
            for line in f:
                if line.startswith('import ') or line.startswith('from '):
                    tokens = line.split()
                    if len(tokens) >= 2:
                        library_name = tokens[1].split('.')[0]  # Para manejar imports de submódulos
                        external_libraries.add(library_name)

    # Paso 2: Mapeo de imports a bibliotecas de terceros
    # Aquí asumimos que ya tienes un diccionario que mapea los imports a sus bibliotecas correspondientes
    # En este ejemplo, llamaremos a este diccionario 'import_to_library'

    # Paso 3: Asociación de bibliotecas con propietarios y gerentes
    owners_of_libraries = {}
    for library_name in external_libraries:
        owner = find_owner_for_library(library_name)  # Implementa esta función para encontrar el propietario
        owners_of_libraries[library_name] = owner

    managers_of_libraries = {}
    for library_name, owner in owners_of_libraries.items():
        project = session.query(Project).filter_by(owner=owner).first()
        if project:
            managers_of_libraries[library_name] = project.manager

    # Ahora 'managers_of_libraries' contendrá un mapeo de cada biblioteca de terceros a su gerente asociado
