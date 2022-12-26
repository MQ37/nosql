from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from webapp.flaskr.map import bp
from webapp.flaskr.db import neo4j
from webapp.flaskr.utils import login_required


@bp.route("/", methods=["POST", "GET"])
@login_required
def index_view():
    if request.method == "GET":
        return render_template("map/index.html", cities=get_cities())
    else:
        path = find_shortest_path(request.form["city1"], request.form["city2"])
        return render_template("map/index.html",
                               cities=get_cities(),
                               path=path)


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

        # Create city nodes if they don't exist and connect them
        create_city_if_not_exists(city1)
        create_city_if_not_exists(city2)
        connect_cities(city1, city2, distance)

        flash("Cities have been successfully connected!", "success")
        return redirect(url_for("map.index_view"))
    else:
        print(get_cities())
        return render_template("map/connect-cities.html", cities=get_cities())


# Get all cities
def get_cities():
    with neo4j.session() as session:
        result = session.run("MATCH (c:City) RETURN c.name")
        return [record["c.name"] for record in result]


def create_city_if_not_exists(city):
    with neo4j.session() as session:
        session.run("MERGE (c:City {name: $city})", {"city": city})


def connect_cities(city1, city2, distance):
    with neo4j.session() as session:
        session.run(
            "MATCH (c1:City {name: $city1}) "
            "MATCH (c2:City {name: $city2}) "
            "MERGE (c1)<-[:CONNECTED_TO]-(h:Highway {distance: $distance})-[:CONNECTED_TO]->(c2)",
            {
                "city1": city1,
                "city2": city2,
                "distance": distance
            })


# find the shortest path between two cities
def find_shortest_path(city1, city2):
    with neo4j.session() as session:
        result = session.run(
            "MATCH (c1:City {name: $city1}), (c2:City {name: $city2}), p = shortestPath((c1)-[:CONNECTED_TO*]-(c2)) "
            "RETURN p", {
                "city1": city1,
                "city2": city2
            })
        print(result.single())
