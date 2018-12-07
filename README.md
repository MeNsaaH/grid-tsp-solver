# RECURSIVE N-MEANS WITH OMNISCIENT POINT

Solving TSP by changing focus to an omniscient director more than a JIT direction

## HOW IT WORKS
- The algorithm tries to segment and direct the movement of the Travelling Salesman from a single centry point
- The points are segmented into grids of equal width and height
- The next point B from current point A is the point with the lowest cost calculated as:

	`The cost from A to B` * `the Cost from A to grid A` * `the cost from grid A to the generic center`

## Costs Breakdown
- *`Cost from A to B`*: This is the Euclidean Distance from point A to Point B
- *`Cost from A to Grid A`*: This is the Euclidean Distance from point A to the center of the Grid where A is in
- *`Cost from Grid A to generic Center`*: This is the Euclidean Distance from grid A to the generic Epicenter of the graph

## TODO

- Convert implementation to Numpy, pandas
- Optimize Calculation