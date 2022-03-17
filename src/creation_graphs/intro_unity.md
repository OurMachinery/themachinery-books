# Creation Graphs for Unity Developers

When a creation graph is used as a surface shader it most closely resembles to Unity's shader graph. This is what we will focus on first.

![Simple surface shader](https://www.dropbox.com/s/lg5dir5rxbz8c6l/tm_guide_creation_graph_unity.png?dl=1)

In the example above the editor's layout was made to resemble Unity's shader graph view. When creating a material shader you need to have a `Shader Instance` output node. From here we can specify our shader by adding node to the left of the `Shader Instance` node. In this example the `Lit` node closely resembles Unity's `PBR Master` node.