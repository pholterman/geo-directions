from fastapi import FastAPI
from src.models.route import RouteInput, RouteResponse
from src.graph import Graph
from src.calculate_travel_time import calculate_travel_time_from_graph

app = FastAPI()

graph = Graph("overijssel.graphml", "Overijssel, NL")
graph.create_graph(False)
G_ig = graph.G_ig
G_nx = graph.G_nx


@app.post("/travel-time/", response_model=RouteResponse)
async def calculate_travel_time(route: RouteInput):
    from_coordinates = route.data.from_coordinates
    to_coordinates = route.data.to_coordinates

    [travel_time, travel_distance] = calculate_travel_time_from_graph(from_coordinates, to_coordinates, G_ig, G_nx)

    return {"data":  {"travel_time": travel_time, "travel_distance": travel_distance}}
