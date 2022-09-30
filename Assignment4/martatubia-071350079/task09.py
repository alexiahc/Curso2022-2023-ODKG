# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NGLbe1YE-fqVGUT1q_lJqwHQhk-qeaPs

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

for s,p,o in g1:
  print(s,p,o)

for s,p,o in g2:
  print(s,p,o)

vcard=Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
n1=Namespace("http://data.three.org#")
n2=Namespace("http://data.four.org#")
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT 
    ?s ?family ?name
  WHERE { 
    ?s rdf:type n1:Person. 
    ?s vcard:Given ?name.
    ?s vcard:Family ?family.
  }
  ''',
  initNs = { "n1": n1, "vcard": vcard}
)

for A in g1.query(q1):
  print(A)

print("Busco esos mismos datos ahora en g2")
q2 = prepareQuery('''
  SELECT 
    ?s  ?family ?name 
  WHERE { 
    ?s rdf:type n2:Person.
    ?s vcard:Given ?name.
    ?s vcard:Family ?family
  }
  ''',
  initNs = { "n2": n2, "vcard": vcard}
)

for B in g2.query(q2):
  print(B)



from rdflib.namespace import OWL
for A in g1.query(q1):
  for B in g2.query(q2):
    if A.family == B.family and A.name == B.name:
      g3.add((A.s, OWL.sameAs, B.s))
      print((A.s, OWL.sameAs, B.s))