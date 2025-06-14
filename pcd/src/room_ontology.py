from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

class RoomOntology:
    def __init__(self):
        self.g = Graph()
        
        # Define namespaces
        self.ROOM = Namespace("http://example.org/room#")
        self.GEO = Namespace("http://www.opengis.net/ont/geosparql#")
        self.CIDOC = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        self.BOT = Namespace("https://w3id.org/bot#")
        
        # Bind namespaces
        self.g.bind("room", self.ROOM)
        self.g.bind("geo", self.GEO)
        self.g.bind("cidoc", self.CIDOC)
        self.g.bind("bot", self.BOT)
        
        self._define_classes()
        self._define_properties()
    
    def _define_classes(self):
        # Physical Objects
        self.g.add((self.ROOM.PhysicalObject, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Wall, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Wall, RDFS.subClassOf, self.ROOM.PhysicalObject))
        self.g.add((self.ROOM.Floor, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Floor, RDFS.subClassOf, self.ROOM.PhysicalObject))
        self.g.add((self.ROOM.Furniture, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Furniture, RDFS.subClassOf, self.ROOM.PhysicalObject))
        
        # Spatial Location
        self.g.add((self.ROOM.SpatialLocation, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Room, RDF.type, OWL.Class))
        self.g.add((self.ROOM.Room, RDFS.subClassOf, self.ROOM.SpatialLocation))
        
        # Material
        self.g.add((self.ROOM.Material, RDF.type, OWL.Class))
        
        # Topological Relations
        self.g.add((self.ROOM.TopologicalRelation, RDF.type, OWL.Class))
    
    def _define_properties(self):
        # Object Properties
        self.g.add((self.ROOM.isLocatedIn, RDF.type, OWL.ObjectProperty))
        self.g.add((self.ROOM.hasMaterial, RDF.type, OWL.ObjectProperty))
        self.g.add((self.ROOM.touches, RDF.type, OWL.ObjectProperty))
        self.g.add((self.ROOM.inside, RDF.type, OWL.ObjectProperty))
        self.g.add((self.ROOM.supportedBy, RDF.type, OWL.ObjectProperty))
        
        # Data Properties
        self.g.add((self.ROOM.hasHeight, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.ROOM.hasWidth, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.ROOM.hasDepth, RDF.type, OWL.DatatypeProperty))
        self.g.add((self.ROOM.hasColor, RDF.type, OWL.DatatypeProperty))
    
    def add_physical_object(self, obj_id, obj_type, properties=None):
        """Add a physical object to the ontology"""
        obj_uri = self.ROOM[obj_id]
        self.g.add((obj_uri, RDF.type, obj_type))
        
        if properties:
            for prop, value in properties.items():
                if isinstance(value, URIRef):
                    self.g.add((obj_uri, self.ROOM[prop], value))
                else:
                    self.g.add((obj_uri, self.ROOM[prop], Literal(value)))
    
    def add_spatial_relation(self, obj1_id, relation, obj2_id):
        """Add a spatial relation between two objects"""
        obj1_uri = self.ROOM[obj1_id]
        obj2_uri = self.ROOM[obj2_id]
        self.g.add((obj1_uri, self.ROOM[relation], obj2_uri))
    
    def query(self, sparql_query):
        """Execute a SPARQL query on the ontology"""
        return self.g.query(sparql_query)
    
    def save(self, filename):
        """Save the ontology to a file"""
        self.g.serialize(destination=filename, format="turtle") 