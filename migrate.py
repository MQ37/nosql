from neo4j import GraphDatabase

# Connect to the database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mypassword"))

with driver.session() as session:
  # Empty the database
  session.run("MATCH (n) DETACH DELETE n")

  # Create city nodes
  # Czech and German and Poland cities connected by highways and their distances
  connected_cities = [
    ("Prague", "Brno", 207), ("Brno", "Ostrava", 165), ("Ostrava", "Wroclaw", 248), ("Wroclaw", "Berlin", 350),
    ("Berlin", "Dresden", 143), ("Dresden", "Prague", 190), ("Prague", "Wroclaw", 350),
    ("Wroclaw", "Katowice", 174), ("Katowice", "Krakow", 218), ("Katowice", "Lodz", 174), ("Lodz", "Warsaw", 174),
    ("Lodz", "Poznan", 174), ("Poznan", "Berlin", 350), ("Prague", "Munich", 382), ("Munich", "Dresden", 460)
  ]
  
  # Create city nodes if they don't exist
  for city1, city2, distance in connected_cities:  
    session.run(
      "MERGE (a:City {name: $city1}) MERGE (b:City {name: $city2})",
      {"city1": city1, "city2": city2}
    )

    # Create a highway node between the cities
    session.run(
      "MATCH (a:City {name: $city1}), (b:City {name: $city2}) " + 
      "CREATE (a)<-[:IS_CONNECTED_TO]-(h:Highway {distance: $distance})-[:IS_CONNECTED_TO]->(b)",
      {"city1": city1, "city2": city2, "distance": distance}
    )
