"""
DS4300 HW4 - Graph API using Redis
"""

import redis


class GraphAPI:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def reset(self):
        """Flush the database."""
        self.r.flushdb()

    def add_node(self, name, node_type, properties=None):
        """Add a node with a given name, type, and optional properties."""
        node_key = f"node:{name}"
        self.r.hset(node_key, "type", node_type)
        if properties:
            for k, v in properties.items():
                self.r.hset(node_key, k, v)
        # Track node in a set of all nodes of this type
        self.r.sadd(f"nodes:{node_type}", name)

    def add_edge(self, name1, name2, edge_type):
        """Add a directed edge from name1 to name2 of a given type."""
        # Store adjacency: node name1 has an outgoing edge of edge_type to name2
        self.r.sadd(f"edges:{name1}:{edge_type}", name2)
        # Also track all edge types from name1
        self.r.sadd(f"edge_types:{name1}", edge_type)

    def get_adjacent(self, name, node_type=None, edge_type=None):
        """Get names of adjacent nodes, optionally filtered by node type and/or edge type."""
        if edge_type:
            edge_types = [edge_type]
        else:
            edge_types = list(self.r.smembers(f"edge_types:{name}"))

        neighbors = set()
        for et in edge_types:
            neighbors.update(self.r.smembers(f"edges:{name}:{et}"))

        if node_type:
            filtered = set()
            for neighbor in neighbors:
                ntype = self.r.hget(f"node:{neighbor}", "type")
                if ntype == node_type:
                    filtered.add(neighbor)
            return filtered

        return neighbors

    def get_recommendations(self, name):
        """Get books bought by people the given person knows,
        excluding books already purchased by that person."""
        # Books this person already bought
        owned = self.get_adjacent(name, node_type='Book', edge_type='bought')

        # People this person knows
        friends = self.get_adjacent(name, node_type='Person', edge_type='knows')

        # Books bought by friends
        recommended = set()
        for friend in friends:
            friend_books = self.get_adjacent(friend, node_type='Book', edge_type='bought')
            recommended.update(friend_books)

        # Exclude already owned
        recommended -= owned
        return recommended
