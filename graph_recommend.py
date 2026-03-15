"""
DS4300 HW4 - Demonstrate Graph API by building the person/book network
and getting book recommendations for Spencer.
"""

from graph_api import GraphAPI

def main():
    g = GraphAPI()
    g.reset()

    # people nodes
    g.add_node('Emily', 'Person', {'name': 'Emily'})
    g.add_node('Spencer', 'Person', {'name': 'Spencer'})
    g.add_node('Brendan', 'Person', {'name': 'Brendan'})
    g.add_node('Trevor', 'Person', {'name': 'Trevor'})
    g.add_node('Paxton', 'Person', {'name': 'Paxton'})

    # book nodes
    g.add_node('Cosmos', 'Book', {'title': 'Cosmos', 'price': 17.00})
    g.add_node('Database Design', 'Book', {'title': 'Database Design', 'price': 195.00})
    g.add_node('The Life of Cronkite', 'Book', {'title': 'The Life of Cronkite', 'price': 29.95})
    g.add_node('DNA and you', 'Book', {'title': 'DNA and you', 'price': 11.50})

    # bought edges
    g.add_edge('Emily', 'Database Design', 'bought')
    g.add_edge('Spencer', 'Cosmos', 'bought')
    g.add_edge('Spencer', 'Database Design', 'bought')
    g.add_edge('Brendan', 'Database Design', 'bought')
    g.add_edge('Brendan', 'DNA and you', 'bought')
    g.add_edge('Trevor', 'Cosmos', 'bought')
    g.add_edge('Trevor', 'Database Design', 'bought')
    g.add_edge('Paxton', 'Database Design', 'bought')
    g.add_edge('Paxton', 'The Life of Cronkite', 'bought')

    # knows edges
    g.add_edge('Emily', 'Spencer', 'knows')
    g.add_edge('Spencer', 'Emily', 'knows')
    g.add_edge('Spencer', 'Brendan', 'knows')

    # test queries
    print("People Spencer knows")
    friends = g.get_adjacent('Spencer', node_type='Person', edge_type='knows')
    print(friends)

    print("Books Spencer bought")
    books = g.get_adjacent('Spencer', node_type='Book', edge_type='bought')
    print(books)

    print("Book recommendations for Spencer")
    recs = g.get_recommendations('Spencer')
    print(recs)
    # should get DNA and you - Emily and Brendan's other books are ones Spencer already has


if __name__ == '__main__':
    main()
