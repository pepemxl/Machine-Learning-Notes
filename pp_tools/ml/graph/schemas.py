"""
    Full list of references:
        https://schema.org/docs/full.html
    Recommended:
        - schema_action = Namespace("https://schema.org/Action")
        - schema_category_code = Namespace("https://schema.org/CategoryCode")
        - schema_category_code_set = Namespace("https://schema.org/CategoryCodeSet")
        - schema_computer_language = Namespace("https://schema.org/ComputerLanguage")
        - schema_defined_term = Namespace("https://schema.org/DefinedTerm")
        - schema_event = Namespace("https://schema.org/Event")
        - schema_intangible = Namespace("https://schema.org/Intangible")
        - schema_library_system = Namespace("https://schema.org/LibrarySystem")
        - schema_math_solver = Namespace("https://schema.org/MathSolver")
        - schema_mobile_application = Namespace("https://schema.org/MobileApplication")
        - schema_organization = Namespace("https://schema.org/Organization")
        - schema_person = Namespace("https://schema.org/Person")
        - schema_product = Namespace("https://schema.org/Product")
        - schema_schedule = Namespace("https://schema.org/Schedule")
        - schema_service = Namespace("https://schema.org/Service")
        - schema_software_application = Namespace("https://schema.org/SoftwareApplication")
        - schema_software_source_code = Namespace("https://schema.org/SoftwareSourceCode")
        - schema_solve_math_action = Namespace("https://schema.org/SolveMathAction")
        - schema_thing = Namespace("https://schema.org/Thing")
        - schema_web_api = Namespace("https://schema.org/WebAPI")
        - schema_web_page = Namespace("https://schema.org/WebPage")

"""
from rdflib import Graph
from rdflib import Namespace
from rdflib import Literal
from rdflib import RDF
from rdflib import URIRef
if __name__  == '__main__':
    import os
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import APP_NAME


def get_schema_from_namespace(name:str = "http://schema.org/"):
    schema = Namespace(name)
    g = Graph()
    schema_org_url = "https://schema.org/docs/schemaorg.owl"
    g.parse(schema_org_url, format='xml')
    return schema, g

def get_schema_from_schema_org(g_schema_org):
    # Consulta de ejemplo para recuperar todas las clases
    query = """
    SELECT DISTINCT ?class WHERE {
        ?class a rdfs:Class .
        FILTER(STRSTARTS(STR(?class), "http://schema.org/"))
    }
    """
    # Ejecutar la consulta y mostrar los resultados
    for row in g_schema_org.query(query):
        print(row.class)


def test_schema(schema, g_schema_org):
    print(schema)
    print(schema.Product)
    print(schema.SoftwareApplication)
    print(schema.LoQueSeMePegueLaGana)
    print(schema.name)
    # # Crear una instancia de una clase de Schema.org
    producto_url = URIRef("http://example.org/product/1")
    # # source_code = 
    g_producto = Graph()
    g_producto.add((producto_url, RDF.type, schema.Service))
    # # Asignar propiedades a la instancia
    g_producto.add((producto_url, schema.name, Literal("Producto de ejemplo")))
    g_producto.add((producto_url, schema.description, Literal("Descripción del producto de ejemplo")))
    g_producto.add((producto_url, schema.price, Literal("19.99")))
    print(len(g_producto))
    print(g_producto.serialize(format='turtle').encode('utf-8'))
    for s, p, o in g_producto:
        print((s, p, o))
    


if __name__ == '__main__':
    schema, g_schema_org = get_schema_from_namespace(APP_NAME)
    get_schema_from_schema_org(g_schema_org)
    test_schema(schema, g_schema_org)
