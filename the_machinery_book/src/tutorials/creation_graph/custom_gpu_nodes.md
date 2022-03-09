# Custom GPU nodes

The [*Creation Graph*]({{the_machinery_book}}/creation_graphs/concept.html) is a powerful visual scripting language that can generate shader code through its GPU nodes. Extending this with custom nodes allows for more complex algorithms, custom material types and much more. In this tutorial we will demonstrate how to create some basic GPU nodes. To learn the difference between CPU and GPU nodes, check out [*Node Types*]({{the_machinery_book}}/creation_graphs/node_types.html). 

A creation graph GPU node needs to be in a `.tmsl` file, these can be compiled by the shader system. Note that there can only be **one** creation graph node per `.tmsl` file, additional definitions will be ignored. If these shaders are placed in the `bin/data/shaders/` directory, they will be loaded automatically.  `.tmsl` files are written in a Simplified JSON format with less strict punctuation requirements. For a full reference on the shader files, check out the [Shader System Reference]({{docs}}doc/shader_system_reference.md.html).


## Cube Node
![](https://www.dropbox.com/s/z6faxvwm0sb7i9o/tut_creation_graph_custom_cube.png?dl=1)

```json
function: [[
	output.res = x * x * x;
]]

creation_graph_node: {
	name: "tm_cube_node"
	display_name: "Cube"
	category: "Shader/Math"

	inputs: [ 
		{ name: "x" display_name: "X" } 
	]
	outputs: [
		{ name: "res" display_name: "Result" type: { type_of: "x" } }
	]
}
```

This node shows you the absolute basics of making a creation graph GPU node. All GPU nodes require two blocks. The `function` block is where you put the actual shader code. The `creation_graph_node` is a meta node that defines node I/O and general information.

In this example, the `creation_graph_node` has several fields, but more can be defined:

- `name` must be a unique identifier for the node. It’s a good idea to prefix this with your namespace to make sure it doesn't inadvertently collide with nodes created by other people.
- `display_name` is optional and specifies node name to show in the UI. If this is empty, a display name will be generated from the `name` field.
- `category` is an optional path-type string that allows you to group related nodes.
- `inputs` is an array of input parameters for the node. A type can be specified for each parameter but it is not required. If you don't specify a type, the type will be generic.
- `outputs` is an array of output values for the node.

Note that we didn’t specify a `type` parameter for our input field. This makes it a fuzzy input and anything that supports the multiplication operator can be passed. Our output parameter does have a `type` field, but instead of defining a fixed type, it uses a generic syntax that sets the output type to whatever the input type was. For more information about this syntax see the [Shader System Reference]({{docs}}doc/shader_system_reference.md.html).



## Depth Output Node
![](https://www.dropbox.com/s/o947fbjy9uddltn/tut_creation_graph_custom_depth_output.png?dl=1)


Output nodes are more complex than function nodes. Instead of a single `function` block, these nodes take the form of a render pass that can have variations based on the systems used with it and the connected inputs. The example above creates a very simple material node that displays a gray-scale interpretation of the object’s distance to the viewing camera.

```json
depth_stencil_states: {
	depth_test_enable: true
	depth_write_enable: true
	depth_compare_op: "greater_equal"
}

raster_states: {
	front_face: "ccw"
}

imports: [
	{ name: "tm" type: "float4x4" }
]

vertex_shader: {
	import_system_semantics: [ "vertex_id" ]

	code: [[
		tm_vertex_loader_context ctx;
		init_vertex_loader_context(ctx);
		float4 vp = load_position(ctx, vertex_id, 0);

		float4 wp = mul(vp, load_tm());
		output.position = mul(wp, load_camera_view_projection());
		return output;
	]]
}

pixel_shader: {
	code: [[
		float2 near_far = load_camera_near_far();
		float depth = linearize_depth(input.position.z, near_far.x, near_far.y) * 0.01f;

		output.buffer0 = float4(linear_to_gamma2(depth), 1); // Base color, alpha
		output.buffer1 = float4(1, 1, 0, 1); // Normal (encoded in signed oct)
		output.buffer2 = float4(0, 0, 0, 1); // Specular, Roughness
		output.velocity = float2(0, 0);
		return output;
	]]
}
```

The `creation_graph_node` block for this node is very small. If no outputs are specified, the output will be a `Shader Instance`. These can be passed to other nodes for rendering, like the `Draw Call` and `Shader Instance` output nodes.

```json
creation_graph_node: {
	name: "depth_output"
	display_name: "Depth"
	category: "Shader/Output"
}
```

In this example the `compile` block has the following fields:

- `includes` specifies which common shaders this shader is dependent on. In this example, that is the `common.tmsl` shader because we use the `linear_to_gamma2()` function from that shader.
- `contexts` specifies how this pass should be executed depending on the context. In this example, we only support one context, the `viewport`. In this context, we want to run during the `gbuffer` phase so we specify that as our layer. We also want to enable the `gbuffer_system` as we will be writing to it. Finally we specify that in this context we will enable the `gbuffer` configuration.
- `configurations` are groups of settings. In this example we have one configuration group: `gbuffer`. This configuration requests three systems, if these systems are not present then we cannot run:
    - The `viewer_system` is needed to query the camera information.
    - The `gbuffer_system` allows us to render to the G-Buffer in the opaque pass of the default render pipeline.
    - The `vertex_buffer_system` allows us to query vertex information from the mesh.

```json
compile: {
	includes: [ "common" ]

	configurations: {
		gbuffer: [{ 
			variations: [{ 
				systems: [ "viewer_system", "gbuffer_system", "vertex_buffer_system" ]
			}]
		}]
	}

	contexts: {
		viewport: [
			{ layer: "gbuffer" enable_systems: [ "gbuffer_system" ] configuration: "gbuffer" }
		]
	}
}
```

> **Note** that the available contexts are defined by the application. Some examples of these in The Machinery editor are `viewport`, `shadow_caster` and `ray_trace_material`. 

> **Note** that the layers are defined by the render pipeline used. Some examples from the default render pipeline are: `gbuffer`, `skydome`, `hdr-transparency`, `ui`. 

