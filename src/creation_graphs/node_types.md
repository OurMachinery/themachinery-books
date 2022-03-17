# Node types

Nodes in the creation graph can be subdivided into four types, understanding the difference between these nodes is important when creating new nodes. The diagram below shows how each node can be categorized.

![](https://www.dropbox.com/s/h4uni5g7syk0zgn/tm_guide_creation_graph_node_types_graph.png?dl=1)


GPU nodes are somewhat special as they will be compiled down into a single shader instead of being interpreted like the CPU part of the creation graph. Note that GPU nodes also have a different background color to distinguish them. GPU nodes will not connect to any CPU node unless their output is a `Shader Instance`, this is the point at which the GPU portion of the graph is compiled and passed to the CPU.

The CPU portion of a creation graph is very similar to the entity graph in terms of layout with one exception. The creation graph often works by querying `output nodes` from the creation graph and working its way back from there. `event nodes` on the other hand allow you to follow the same flow as the entity graph, beginning from some event and continuing into other nodes. 

![](https://www.dropbox.com/s/poi2rg73gttdixz/tm_guide_creation_graph_node_types_practical.png?dl=1)

In the example above you can see a creation graph that uses the `Draw Call` and `Bounding Volume` output nodes. A Creation Graph with these kinds of nodes is commonly found living under the Render Component, since such a componen will automatically process any draw calls. The inputs to this graph are: a DCC mesh and a `Lit Shader Instance`, where the latter can be thought of as a shader or material. Note the `Variable` GPU node that is used to pass the color from the CPU side to the GPU side, this is the only way to connect CPU nodes to GPU nodes.
Currently we support the following output nodes, note that multiple of these can be present in a single creation graph.

| **Name**                           | **Information**                                                 |
| ---------------------------------- | --------------------------------------------------------------- |
| Image Output                       | Often used by Image assets and can be supplied to materials as textures etc. Allows preview of the Image. |
| Bounding Volume                    | Used for culling.                                               |
| Draw Call                          | Generally used with the `Render Component`, allows preview.     |
| Shader Instance                    | Can be used as a material, allows preview.                           |
| Physics Shape                      | Generally used with a `Physics Shape Component`.                |
| Ray Trace Instance                 | Used to generate acceleration structures and hit shaders.       |
| Entity Spawner - Output Transforms | Can be used to query transforms from the `Entity Spawner` node. |