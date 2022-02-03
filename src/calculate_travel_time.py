from osmnx.distance import nearest_nodes
from networkx import MultiDiGraph
from igraph import Graph

def calculate_travel_time_from_graph(from_str: str, to_str: str, igraph: Graph, networkx_graph: MultiDiGraph) -> [float, float]:
    from_coord = tuple(map(float, from_str.split(',')))
    to_coord = tuple(map(float, to_str.split(',')))

    # find nodes based on coordinates in networkx graph
    source = nearest_nodes(networkx_graph, from_coord[1], from_coord[0])
    destination = nearest_nodes(networkx_graph, to_coord[1], to_coord[0])

    # find corresponding nodes (vertices) in igraph graph
    source = igraph.vs.select(name=source)
    destination = igraph.vs.select(name=destination)

    # calculate shortest path based on travel time
    shortest_path = igraph.get_shortest_paths(source[0].index, to=destination[0].index, weights="travel_time")

    # calculate total travel time and travel distance
    i_prev = 0
    travel_time = 0
    travel_distance = 0
    for i in shortest_path[0]:
        if i_prev > 0:
            travel_time += igraph.es.select(_between=([i_prev],[i]))[0]["travel_time"]
            travel_distance += igraph.es.select(_between=([i_prev], [i]))[0]["length"]
        i_prev = i

    return [travel_time, travel_distance]