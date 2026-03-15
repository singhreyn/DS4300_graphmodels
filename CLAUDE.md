# DS4300 HW4 - Graph Data Models

## Assignment Overview
Model graphs in both a relational database (MySQL) and Redis.

## Part I: SQL Queries (graph_queries.sql)
Write SQL queries against a generic graph schema (node, edge, node_props tables):
- a. Sum of all book prices (don't assume only books have prices)
- b. What people does Spencer know? (don't assume only people can be "known")
- c. What books did Spencer buy? (title and price)
- d. What people know each other? (pairs of names)
- e. Recommendation engine: books bought by people Spencer knows, excluding Spencer's books

## Part II: Redis Graph API (Python)
- `graph_api.py` - API with: add_node, add_edge, get_adjacent, get_recommendations
- `graph_recommend.py` - Demo script that builds the graph and gets recommendations for Spencer

## Deliverables
1. `graph_queries.sql` - SQL queries
2. `graph_output.txt` - Query output (or embedded as comments)
3. `graph_api.py` - Redis graph API
4. `graph_recommend.py` - Demo/test script

## Schema (from graph_start.sql)
- `node(node_id, type)`
- `edge(edge_id, in_node, out_node, type)`
- `node_props(node_id, propkey, string_value, num_value)`
