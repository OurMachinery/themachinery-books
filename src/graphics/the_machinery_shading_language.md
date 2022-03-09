# The Machinery Shader Language

Shaders in The Machinery are defined using The Machinery Shader Language (`tmsl`). Traditionally shaders (like those written in `glsl` or `hlsl`) only contain the shader code itself and some I/O definitions. The Machinery (like other engines) stores not only the shader code, but also the pipeline state in its shader files. Additionally The Machinery allows shaders to define variations and systems that allow for more complex shader generation and combinations. For a complete list of what can be in a `tmsl` file see the [Shader System Reference](https://ourmachinery.com/apidoc/doc/shader_system_reference.md.html). For an in depth look at the design goals of these shader files see [The Machinery Shader System](https://ourmachinery.com/post/the-machinery-shader-system-part-1/) blog posts.

A shader file can be divided into three distinct sections:

- Code blocks, these define [HLSL](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl) code blocks that contain the main shader code.
- Pipeline state blocks, these define the Pipeline State Objects (PSO) or shader environment required for the code to run. 
- Compilation blocks, these define meta information about how the shader should be compiled. This also allows for multiple variations of shaders, for instance one with multi-sampling enabled and one with multi-sampling disabled.

Let’s have a look at a `Hello Triangle` shader for The Machinery.

```json
imports: [
    { name: "color" type: "float3" }
]

vertex_shader: {
    import_system_semantics : [ "vertex_id" ]

    code: [[
        const float2 vertices[] = {
            float2(-0.7f, 0.7f),
            float2(0.7f, 0.7f),
            float2(0.0f, -0.7f)
        };

        output.position = float4(vertices[vertex_id], 0.0f, 1.0f);
        return output;
    ]]
}

pixel_shader: {
    code: [[
        output.color = load_color();
        return output;
    ]]
}

compile: {}
```

In this example we have some shader code, no explicit pipeline state, and an empty compile block. The first thing to note is that `tmsl`  files use a JSON like format. The main sections of code are the `vertex_shader` and the `pixel_shader` blocks. Within these are `code` blocks which specify the HLSL code that needs to run at the relative pipeline stage. In this example we create a screen-space triangle from three constant vertices and give it a color passed on as an input.

If we want to pass anything to a shader we need to define it in the `imports` block. Anything defined in here will be accessible though `load_#` or `get_#` functions. See the [Shader System Reference](https://ourmachinery.com/apidoc/doc/shader_system_reference.md.html) for more information.

We also need to define a `compile` or `system` block in order for our shader to be compiled. If neither block is defined then the shader is assumed to be a library type shader which can be included into other shaders. 

> **Note:** You can find all built-in shaders in the folder: `./bin/data/shaders/` in the shipped engine (for source code access this is: `./the_machinery/shaders/`).


## Procedural shaders

Note that shaders don’t have to be written and compiled in this way. You can generate shaders directly from code using the `tm_shader_repository_api`. You can create a new shader declaration by calling `create_shader_declaration()`, populate it with your custom code by using the `tm_shader_declaration_api`, and compile it using `create_from_declaration()`. Any `tmsl` file will go through the same pipeline. 


> **Note:** Shader are also used to create GPU nodes for the Creation Graph, see Creation Graph: [Shader System Interaction]({{base_url}}/creation_graphs/shader_system.html) for more information.



