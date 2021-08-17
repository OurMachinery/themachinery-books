# Shaders

The Creation Graph provides an artist-friendly way to create custom shaders by wiring together nodes into a shader network. Each node in the graph represents a snippet of HLSL code that gets combined by the shader system plugin into full HLSL programs. It can sometimes be nice to work directly with HLSL code for more advanced shaders, either by exposing new helper nodes to the Creation Graph or by directly writing a complete shader program in HLSL. This is typically done by adding new `.tmsl` files (where `tmsl` stands for `The Machinery Shading Language`) that The Machinery loads on boot up.

A `.tmsl` file is essentially a data-driven JSON front-end for creating and populating a `tm_shader_declaration_o` structure which is the main building block that the compiler in shader system plugin operates on. While a `tm_shader_declaration_o` can contain anything needed to compile a complete shader (all needed shader stages, any states and input/output it needs, etc), it is more common that they contain only fragments of and multiple `tm_shader_declaration_o` are combined into the final shader source that gets compiled into a `tm_shader_o` that can be used when rendering a draw call (or dispatching a compute job).



> **Note:** You can find all built-in shaders in the folder: `./bin/data/shaders` shipped with your engine version. (For source access: `./the_machinery/shaders`)



Inserting the `creation_graph` block in the `.tmsl` file will get exposed as a node in the Creation Graph. Nodes exposed to the Creation Graph can either be *function* nodes (see: `data/shaders/nodes/`) or *output* nodes (see: `data/shaders/output_nodes/`). A *function* node won't compile into anything by itself unless it's connected to an *output* node responsible for declaring the actual shader stages and evaluating the branches of connected *function* nodes.



>  **Note:** More information about creating creation graph nodes you can find in the Creation Graph Section:
>
> - [Node Types]({{the_machinery_book}}/creation_graphs/node_types.html)
>
> - [Shader system interaction]({{the_machinery_book}}/creation_graphs/shader_system.html)
>
> - [Create custom GPU node Tutorial]({{tutorials}}/creation_graph/custom_gpu_nodes.html)



Typically these are function nodes (see `data/shaders/nodes`) that won't compile into anything without getting connected to an "output" node. We ship with a few built-in output nodes (see `data/shaders/output_nodes`) responsible for declaring the actual shader stages and glue everything together. 

>  **Note:** For more details on the Shader Language itself, please check the [Shader Reference](https://ourmachinery.com/apidoc/doc/shader_system_reference.md.html) or the Chapter [The Machinery Shading Language]({{the_machinery_book}}/the_machinery_shading_language.md).

The whole Shader System is explained in more detail within these posts:

- [The Machinery Shader System (part 1)](https://ourmachinery.com/post/the-machinery-shader-system-part-1/)
- [The Machinery Shader System (part 2)](https://ourmachinery.com/post/the-machinery-shader-system-part-2/)
- [The Machinery Shader System (part 3)](https://ourmachinery.com/post/the-machinery-shader-system-part-3/)
- [Efficient binding of shader resources](https://ourmachinery.com/post/efficient-binding-of-shader-resources/)