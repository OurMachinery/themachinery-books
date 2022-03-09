# Creation Graphs

The creation graph is (as the name implies) a graph based tool for creating assets. It allows developers to define and alter various types of assets using visual scripting. More broadly speaking, the creation graph can be used for arbitrary data processing tasks.

A creation graph thus defines the asset’s pipeline into its final state. For instance, an image asset will have a file that defines the data of the image, but the creation graph asset specifies how that data should be processed. Should it generate mipmaps, should it be compressed, do we need a CPU copy of it, etc.

A more familiar example might be a material shader. In The Machinery this is also defined using a creation graph. This case maps very well to Unity’s shader assets and Unreal’s material assets. In the image below you can see a simple default material with a saturated red base color.

![Simple red material](https://www.dropbox.com/s/w5ty4r8tttntt0t/tm_guide_creation_graph_simple_material.png?dl=1)


Image loading and material creation are just a few examples of what can be achieved with the creation graph. The table below shows when a creation graph is used compared to the tools one could use in Unity and Unreal.

| Asset Type           | Unity                | Unreal      | The Machinery                   |
| -------------------- | -------------------- | ----------- | ------------------------------- |
| Images               | Texture              | Texture     | Creation graphs                 |
| Materials            | Shader               | Material    | Creation graphs                 |
| Particles            | Particle Effect      | Cascade     | Creation graphs                 |
| Post processing      | Shader               | Material    | Creation graphs                 |
| Procedural materials | Procedural Materials | Material    | Creation graphs                 |
| Meshes               | Mesh                 | Static Mesh | DCC Asset + <br>Creation graphs |

Another example for the creation graph is mesh processing. A graph like this will define how the mesh should be draw or traced against. The graph below takes two inputs, a material creation graph and the mesh data from a DCC asset. This data is than imported and passed to the various outputs of our mesh pipeline. In this case those are: a ray tracing instance, a normal draw call, a bounding volume, and a physics shape. Note that not all of these outputs have to be used, rather the code that uses this creation graph might only look for the rendering outputs and ignore the physics shape, whilst some other code might only care about the physics shape output.

![Mesh processing](https://www.dropbox.com/s/103bvtqaz6lnsog/tm_guide_creation_graph_mesh_processing.png?dl=1)


Like the entity graph, the creation graph can executes nodes in sequence from an event. Some examples of this are the `Tick`, `Init`, and `Compile` events which are executed at known intervals. Most of the creation graphs however work with a reverse flow, compiling the graph into a sequence of nodes for a specific output. The two examples presented earlier show this workflow. Some outputs are: `Draw Call`, `Shader Instance`, `Image`, and `Physics Shape`. Note that these outputs are just blobs of data, an implementation can define more output type in code.


