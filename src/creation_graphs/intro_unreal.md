# Creation Graphs for Unreal Engine developers

Creation graphs are used for many different assets in The Machinery. When a creation graph is used for a shader it most closely relates to Unreal’s materials (any domain). This is what we will focus on first.

![Simple brick material](https://www.dropbox.com/s/nxy6jtq7f5drmin/tm_guide_creation_graph_unreal_material.png?dl=1)


In the example above the editor closely resembles the material editor from Unreal, this is however not the default layout. You can see the creation graph in the center with its output being a `Shader Instance`. Adding this allows any consuming code to query the material from this creation graph and it will allow the preview tab to display your material. 

![Simple rotating particle](https://www.dropbox.com/s/kpf05fwzl47d0ip/tm_guide_creation_graph_unreal_particle.png?dl=1)


The previous example showed a surface or material shader. This example shows a creation graph that fully defines a simple particle. The `Shader Instance` (material) is now passed to a `Draw Call` node, with this combination we can now fully render the particle without the need of an explicit mesh. Instead we use the `Construct Quad` node for a procedural quad mesh. Note that we specify the `Instance Count` and `Num Vertices` (for a single quad that is 6).