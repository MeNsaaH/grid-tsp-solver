# Solving TSP:
### By Mmadu Manasseh

## GRID WITH OMNISCIENT REFERENCE POINT 

Solving Approximate first time TSP by changing focus to an omniscient director more than a JIT direction used by Greedy Algorithm. This algorithm uses a grid system to try to generate a first route of locations optimal than the greedy algorithm. 

Grids are used to divide the points to be routed. This makes each grids contain points which are closer to say.
Movement from one point to another then is dictated by how close the two points are, how close their grid locations are and how close the grid is from the local omniscient point.

The Omniscient Reference point serves as a reference to the density of the remaining points. This helps to make sure a movement from one point to another is not done towards the closest point, but also towards a point where another point is located closely. The tries to avoid extreme points in the case of the Greedy algorithm. 

### Future Adjustment
The Algorithm will be also incorporated with a cost to determine how relatively far the points move from the start point. Another important factor in the TSP is the last point to arrive before getting to the start point. For the Greedy algorithm, sometimes the point is far from the start point. 

A cost factor will be introduced to ensure that at 1/4 completed points, the omniscient point should shift towards the start point. This should make all movement then tend towards the start point while still looking for the closest point.

It's intuitive to say that the algorithm should be kinda intelligent when doing so, but I don't think so 😊

## HOW IT WORKS
I'm not a data scientist 😆, so my cost functions are not efficient to say. We need a better cost function for this to kinda work efficiently

The cost from a point `A` to `B` is computed as thus: 

Cost = `The cost from A to B` * `the Cost from A to grid A` * `the cost from grid A to the generic center`

## Costs Breakdown
- *`Cost from A to B`*: This is the Distance from point A to Point B
- *`Cost from A to Grid A`*: This is the Distance from point A to the center of the Grid where A is in
- *`Cost from Grid A to generic Center`*: This is the Distance from grid A to the generic Epicenter of the graph

## TODO

- Convert implementation to Numpy, pandas
- Optimize Calculation

## ANOTHER-ROUGH-TRY: Recursive k-Means TSP Solver
Another Solution I will like to dive into is a solution that still uses k-means to segment points. A `gnome` is created which maps n locations to itself in such a way that every location it mapped to one `gnome`. Each `gnome` then has an `entry` and an `exit` point and a specified route that leads from the `entry` to the `exit`. 

An upper layer of say `gnomes` are created which maps n `gnomes` of the lower layer to it. And continuously until a layer of high level mapping is established. Movements are dictated from the highest layer level, which are then mapped down the layers to the locations. 

The movements from the `entry` to the `exit` can be established using any algorithm. 
Heuristic Optimization can be applied by shaking a `gnome` in a specific layer and recomputing the cost. 

New ideas are welcomed 🤓