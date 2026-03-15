-- DS4300 HW4 - Graph Queries
-- Part I: Graphs in a Relational Database

use graph;

-- a. What is the sum of all book prices?
-- Don't assume that books are the only thing that could have a price.
SELECT SUM(np.num_value) AS total_book_price
FROM node_props np
JOIN node n ON np.node_id = n.node_id
WHERE n.type = 'Book'
  AND np.propkey = 'price';

-- b. What people does Spencer know?
-- Don't assume that "people" are the only thing one can "know".
SELECT np2.string_value AS name
FROM node_props np1
JOIN node n1 ON np1.node_id = n1.node_id
JOIN edge e ON e.in_node = n1.node_id
JOIN node n2 ON e.out_node = n2.node_id
JOIN node_props np2 ON np2.node_id = n2.node_id
WHERE np1.string_value = 'Spencer'
  AND np1.propkey = 'name'
  AND e.type = 'knows'
  AND n2.type = 'Person'
  AND np2.propkey = 'name';

-- c. What books did Spencer buy? Give title and price.
-- Don't assume books are the only thing that could have a price.
SELECT title.string_value AS title, price.num_value AS price
FROM node_props spencer
JOIN node spencer_node ON spencer.node_id = spencer_node.node_id
JOIN edge e ON e.in_node = spencer_node.node_id
JOIN node book_node ON e.out_node = book_node.node_id
JOIN node_props title ON title.node_id = book_node.node_id AND title.propkey = 'title'
JOIN node_props price ON price.node_id = book_node.node_id AND price.propkey = 'price'
WHERE spencer.string_value = 'Spencer'
  AND spencer.propkey = 'name'
  AND e.type = 'bought'
  AND book_node.type = 'Book';

-- d. What people know each other? Give just a pair of names.
SELECT np1.string_value AS person1, np2.string_value AS person2
FROM edge e1
JOIN edge e2 ON e1.in_node = e2.out_node AND e1.out_node = e2.in_node
JOIN node_props np1 ON np1.node_id = e1.in_node AND np1.propkey = 'name'
JOIN node_props np2 ON np2.node_id = e1.out_node AND np2.propkey = 'name'
WHERE e1.type = 'knows'
  AND e2.type = 'knows'
  AND e1.in_node < e1.out_node;

-- e. Recommendation engine: What books were purchased by people who Spencer knows?
-- Exclude books that Spencer already owns.
SELECT DISTINCT title.string_value AS recommended_book
FROM node_props spencer
JOIN edge knows_edge ON knows_edge.in_node = spencer.node_id
JOIN edge bought_edge ON bought_edge.in_node = knows_edge.out_node
JOIN node book_node ON bought_edge.out_node = book_node.node_id
JOIN node_props title ON title.node_id = book_node.node_id AND title.propkey = 'title'
WHERE spencer.string_value = 'Spencer'
  AND spencer.propkey = 'name'
  AND knows_edge.type = 'knows'
  AND bought_edge.type = 'bought'
  AND book_node.type = 'Book'
  AND book_node.node_id NOT IN (
      SELECT e.out_node
      FROM edge e
      WHERE e.in_node = spencer.node_id
        AND e.type = 'bought'
  );
