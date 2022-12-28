from webapp.flaskr.config import NEO4J_USER, NEO4J_PASSWORD, NEO4J_HOST
from flask_mongoengine import MongoEngine
from neo4j import GraphDatabase

db = MongoEngine()

# Neo4j
graphdb = GraphDatabase.driver("bolt://%s:7687" % NEO4J_HOST,
                               auth=(NEO4J_USER, NEO4J_PASSWORD))
