# Shader system interaction

A creation graph interacts with the shader system in three main ways:

- Its GPU nodes are defined using `.tmsl` shaders.
- GPU output nodes call special linker functions to evaluate the creation graph.
- Shader instances in a creation graph are constructed using the shader system.

The last point is a technical detail that doesn’t matter for anyone extending or using the creation graph so it won’t be covered in this guide. Additional information about the `creation_graph_node` shader block can be found in the [Shader System Reference]({{docs}}doc/shader_system_reference.md.html).

Any GPU node that can be used in the creation graph has an associated `.tmsl` shader file. Most of these can be found here: `the_machinery/shaders/nodes/*.tmsl`. We also supply a [Visual Studio extension](https://marketplace.visualstudio.com/items?itemName=OurMachinery.tmShaderLang) for this file format which adds syntax highlighting, this extension will be used in this guide. 

![](https://www.dropbox.com/s/4o13cq3rzvqm813/tm_guide_creation_graph_sin_node.png?dl=1)


This is the shader code for the `Sin` node. It defines one input (`a`) and one output (`res`, which is the same type as `a`). This shader file will be constructed using the shader system into a single `.hlsl` function. For more information on how to create basic GPU nodes see [Creating custom GPU Nodes]({{tutorials}}creation_graph/custom_gpu_nodes.html).

![](https://www.dropbox.com/s/cs31mi8njs9gpno/tm_guide_creation_graph_linkage.png?dl=1)


This is an example of the shader code needed in the creation graph output nodes. When a creation graph node outputs a `Shader Instance` and has any inputs; it should define these three functions in it’s shader code block so the graph can be evaluated. The `tm_graph_read` function passes all the stage input variables to the graph (like position, color, uv, etc.). The `tm_graph_evaluate` function does most of the work. It uses the `tm_graph_io_t` struct to evaluate the graph by calling the functions generated by the normal nodes. Finally the `tm_graph_write` function passes all the graph variable to the stage output. It is important to note that whilst the `tm_graph_evaluate` function is necessary for graph evaluation; the `tm_graph_read` and `tm_graph_write` are not, they are helper function. For more information on how to create GPU output nodes see [Creating custom GPU Nodes]({{tutorials}}creation_graph/custom_gpu_nodes.html).