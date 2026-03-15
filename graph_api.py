"""
DS4300 HW4 - Graph API using Redis
"""

import redis


class GraphAPI:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def reset(self):
        self.r.flushdb()

    def add_node(self, name, node_type, properties=None):
    # store node as a hash and track it in a set by type
        node_key = f"node:{name}"
        self.r.hset(node_key, "type", node_type)
        if properties:
            for k, v in properties.items():
                self.r.hset(node_key, k, v)
        self.r.sadd(f"nodes:{node_type}", name)

    def add_edge(self, name1, name2, edge_type):
        """Store a directed edge as a set: edges:{name1}:{edge_type} -> {name2, ...}"""
        # Store adjacency: node name1 has an outgoing edge of edge_type to name2
        self.r.sadd(f"edges:{name1}:{edge_type}", name2)
        # track what edge types exist from name1
        self.r.sadd(f"edge_types:{name1}", edge_type)

    def get_adjacent(self, name, node_type=None, edge_type=None):
        """Return adjacent node names. Can filter by node type and/or edge type."""
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
        """Books bought by friends minus books already owned."""
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
