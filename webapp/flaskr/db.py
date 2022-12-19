from flask_mongoengine import MongoEngine
from neo4j import GraphDatabase

db = MongoEngine()

# Neo4j
neo4j = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mypassword"))
