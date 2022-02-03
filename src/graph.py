from osmnx import graph_from_place, config, settings
from osmnx.io import load_graphml, save_graphml
from osmnx import speed, distance
import os
from networkx import MultiDiGraph
from typing import Optional
import igraph as ig
from igraph import Graph, VertexSeq


class Graph:

    file_dir: str = "src/graphs/"
    file_path: str
    query: str = None
    G_ig: Graph
    G_nx: MultiDiGraph

    def __init__(self, file_name: str, query: str = None):
        config(use_cache=True, log_console=True)
        self.file_path = self.file_dir + file_name
        self.query = query

    def load_graph_from_file(self) -> MultiDiGraph:
        return load_graphml(filepath=self.file_path)

    @staticmethod
    def networkx_to_igraph(networkx_graph: MultiDiGraph) -> Graph:
        G = ig.Graph.from_networkx(networkx_graph)
        G.vs["name"] = G.vs["_nx_name"]

        return G

    @staticmethod
    def osmnx_config():
        utn = settings.useful_tags_node
        oxna = settings.osm_xml_node_attrs
        oxnt = settings.osm_xml_node_tags
        utw = settings.useful_tags_way
        oxwa = settings.osm_xml_way_attrs
        oxwt = settings.osm_xml_way_tags
        utn = list(set(utn + oxna + oxnt))
        utw = list(set(utw + oxwa + oxwt))
        config(all_oneway=True, useful_tags_node=utn, useful_tags_way=utw)

    def create_graph(self, reload_graph: bool = False):
        if os.path.exists(self.file_path) and not reload_graph:
            self.G_nx = self.load_graph_from_file()
            speed.add_edge_speeds(self.G_nx, fallback=100, precision=3)
            speed.add_edge_travel_times(self.G_nx, precision=3)
            distance.add_edge_lengths(self.G_nx, precision=3)
            self.G_ig = self.networkx_to_igraph(self.G_nx)

        elif self.query is not None:
            self.G_nx = graph_from_place(self.query, network_type='drive')
            speed.add_edge_speeds(self.G_nx, fallback=100, precision=3)
            speed.add_edge_travel_times(self.G_nx, precision=3)
            distance.add_edge_lengths(self.G_nx, precision=3)
            self.G_ig = self.networkx_to_igraph(self.G_nx)
            # save_graphml(graph, filepath=self.file_path, gephi=False, encoding='utf-8')
            ig.write(self.G_ig, self.file_path, format="graphml")
        else:
            print("something went wrong")
            return None

        self.osmnx_config()


if __name__ == "__main__":

    g = Graph("zwolle_graph.graphml", "Zwolle, NL")
    g.create_graph(reload_graph=False)
    # print(g.G_ig.