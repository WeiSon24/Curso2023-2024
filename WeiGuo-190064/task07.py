# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Tet1MDg3vrBF8KdhZAcfiTlOgf3ttxOD

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# Definir el espacio de nombres para 'ns'
ns = Namespace("http://somewhere#")

from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery(
    """
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
    """,
    initNs={"ns": ns, "rdfs": RDFS}
)

# Ejecutar la consulta y visualizar los resultados
for row in g.query(q1):
    print(row.subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# Tarea 7.2: Listar todos los individuos de "Person" con RDFLib y SPARQL (ten en cuenta las subclases)
q2 = prepareQuery(
    """
    SELECT ?individual
    WHERE {
        ?individual rdf:type/rdfs:subClassOf* ns:Person .
    }
    """,
    initNs={"ns": ns, "rdf": RDF, "rdfs": RDFS}
)

# Ejecutar la consulta y visualizar los resultados
for row in g.query(q2):
    print(row.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# Tarea 7.3: Listar todos los individuos de "Person" o "Animal" y todas sus propiedades, incluyendo su clase
q3 = prepareQuery(
    """
    SELECT ?individual ?property ?value ?class
    WHERE {
        ?individual (rdf:type/rdfs:subClassOf*|rdf:type) ?class .
        ?individual ?property ?value .
        FILTER (?class = ns:Person || ?class = ns:Animal)
    }
    """,
    initNs={"ns": ns, "rdf": RDF, "rdfs": RDFS}
)

# Ejecutar la consulta y visualizar los resultados
for row in g.query(q3):
    print(row.individual)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# Tarea 7.4: Listar el nombre de las personas que conocen a "Rocky"
q4 = prepareQuery(
    """
    SELECT ?name
    WHERE {
        ?person foaf:knows ns:Rocky .
        ?person vcard:fn ?name .
    }
    """,
    initNs={"ns": ns, "foaf": ns.foaf, "vcard": ns.vcard}
)

# Ejecutar la consulta y visualizar los resultados
for row in g.query(q4):
    print(row.name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# Tarea 7.5: Listar las entidades que conocen al menos a otras dos entidades en el grafo
q5 = prepareQuery(
    """
    SELECT ?entity
    WHERE {
        {
            ?entity foaf:knows ?person1 .
            ?entity foaf:knows ?person2 .
            FILTER (?person1 != ?person2)
        } UNION {
            ?entity foaf:knows ?person1 .
            ?entity foaf:knows ?person2 .
            ?entity foaf:knows ?person3 .
            FILTER (?person1 != ?person2 && ?person1 != ?person3 && ?person2 != ?person3)
        }
    }
    GROUP BY ?entity
    HAVING (COUNT(?person1) >= 2)
    """,
    initNs={"ns": ns, "foaf": ns.foaf}
)

# Ejecutar la consulta y visualizar los resultados
for row in g.query(q5):
    print(row.entity)