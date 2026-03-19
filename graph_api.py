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

    # directed edge stored as a set: edges:{name1}:{edge_type} -> {name2, ...}
    def add_edge(self, name1, name2, edge_type):
        self.r.sadd(f"edges:{name1}:{edge_type}", name2)
        # track what edge types exist from name1
        self.r.sadd(f"edge_types:{name1}", edge_type)

    # get neighbors, optionally filtered by node type and/or edge type
    def get_adjacent(self, name, node_type=None, edge_type=None):
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

    # books bought by friends minus books already owned
    def get_recommendations(self, name):
        # books this person already bought
        owned = self.get_adjacent(name, node_type='Book', edge_type='bought')

        # people this person knows
        friends = self.get_adjacent(name, node_type='Person', edge_type='knows')

        # books bought by friends
        recommended = set()
        for friend in friends:
            friend_books = self.get_adjacent(friend, node_type='Book', edge_type='bought')
            recommended.update(friend_books)

        # minus already owned
        recommended -= owned
        return recommended
