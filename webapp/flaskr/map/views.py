from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from webapp.flaskr.map import bp
from webapp.flaskr.db import graphdb
from webapp.flaskr.utils import login_required
import neo4j.exceptions

@bp.route("/", methods=["POST", "GET"])
@login_required
def index_view():
    if request.method == "GET":
        return render_template("map/index.html", cities=get_cities())
    else:
        if request.form["city1"] == request.form["city2"]:
            flash("Please select two different cities!", "danger")
            return redirect(url_for("map.index_view"))

        path, distance = find_shortest_path(request.form["city1"], request.form["city2"])
        return render_template("map/index.html",
                               cities=get_cities(),
                               path=path,
                               distance=distance)


# View for adding a city
@bp.route("/city/add", methods=["POST", "GET"])
@login_required
def add_city_view():
    if request.method == "POST":
        city = request.form["city"]

        # Create city node if it doesn't exist
        create_city_if_not_exists(city)

        flash("The city has been successfully added to the database!",
              "success")
        return redirect(url_for("map.index_view"))
    else:
        return render_template("map/add-city.html")


# View for connecting two cities
@bp.route("/city/connect", methods=["POST", "GET"])
@login_required
def connect_cities_view():
    if request.method == "POST":
        city1 = request.form["city1"]
        city2 = request.form["city2"]
        distance = request.form["distance"]

        # Validate that distnace is a number
        try:
            distance = int(distance)
        except ValueError:
            flash("Distance must be a number!", "danger")
            return redirect(url_for("map.connect_cities_view"))

        # Create city nodes if they don't exist and connect them
        create_city_if_not_exists(city1)
        create_city_if_not_exists(city2)
        connect_cities(city1, city2, int(distance))

        flash("Cities have been successfully connected!", "success")
        return redirect(url_for("map.index_view"))
    else:
        print(get_cities())
        return render_template("map/connect-cities.html", cities=get_cities())


# Get all cities
def get_cities():
    with graphdb.session() as session:
        result = session.run("MATCH (c:City) RETURN c.name")
        return [record["c.name"] for record in result]


def create_city_if_not_exists(city):
    with graphdb.session() as session:
        session.run("MERGE (c:City {name: $city})", {"city": city})


def connect_cities(city1, city2, distance):
    with graphdb.session() as session:
        session.run(
            "MATCH (c1:City {name: $city1}) "
            "MATCH (c2:City {name: $city2}) "
            "MERGE (c1)-[r:HIGHWAY {distance: $distance}]->(c2)",
            {
                "city1": city1,
                "city2": city2,
                "distance": distance
            })


# find the shortest path between two cities
def find_shortest_path(city1, city2):
    with graphdb.session() as session:
        res = session.run("""
        CALL gds.graph.exists('highways')
        """)
        if res.single()["exists"]:
            # Delete the projection if it exists
            session.run("""
            CALL gds.graph.drop('highways')
            """)

        # Create a new projection
        res = session.run("""
        CALL gds.graph.project(
        'highways',
        'City',
        { HIGHWAY: {type: "HIGHWAY", orientation: "UNDIRECTED"}},
        {
        relationshipProperties: 'distance'
        }
        )
        """)

        cmd = """
        MATCH (source:City {name: "%s"}), (target:City {name: "%s"})
        CALL gds.shortestPath.dijkstra.stream('highways', {
            sourceNode: source,
            targetNode: target,
            relationshipWeightProperty: 'distance'
        })
        YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
        RETURN
            index,
            gds.util.asNode(sourceNode).name AS sourceNodeName,
            gds.util.asNode(targetNode).name AS targetNodeName,
            totalCost,
            [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
            costs,
            nodes(path) as path
        ORDER BY index
        """ % (city1, city2)

        res = session.run(cmd)
        rec = res.single()
        
        print("record", rec)

        return [node["name"] for node in rec["path"]], rec["totalCost"]

