from webapp.flaskr.config import NEO4J_USER, NEO4J_PASSWORD
from flask_mongoengine import MongoEngine
from neo4j import GraphDatabase

db = MongoEngine()

# Neo4j
graphdb = GraphDatabase.driver("bolt://localhost:7687",
                               auth=(NEO4J_USER, NEO4J_PASSWORD))
