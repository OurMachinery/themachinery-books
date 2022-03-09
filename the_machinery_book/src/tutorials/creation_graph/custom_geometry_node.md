# Creating Custom Geometry Nodes

In this tutorial we well be creating a CPU node for the [*Creation Graph*]({{the_machinery_book}}/creation_graphs/concept.html) that creates a mesh that can be used by rendering nodes. This tutorial expects some basic knowledge of the creation graph and node creation. it is recommended to read [*Creating custom CPU nodes*]({{tutorials}}/creation_graph/custom_cpu_nodes.html) before reading this.

![](https://www.dropbox.com/s/5xbu16zov1k5h4b/tm_tut_creation_graph_geometry_node.png?dl=1)

The main output of this node will be a `tm_gpu_geometry_t` and a `tm_renderer_draw_call_info_t`. Together these will make out `GPU Geometry` output. Additionally we will be outputting a bounding box for the triangle that can be used for culling and other calculations. But before we can populate those, we’ll need to consider the vertex format of our mesh. For this example, this will be a simple position, normal, and color per vertex:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,custom_geometry_node_data)}}
```

The `tm_renderer_draw_call_info_t` is constant for our example so we can populate it as follows: (note that this node doesn’t create an index buffer and thusly uses `TM_RENDERER_DRAW_TYPE_NON_INDEXED`)

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,custom_geometry_node_call_info)}}
```

Creating the geometry for this node requires us to take several things into consideration. First, we  need to store the vertex buffer, constant buffer, and resource binder somewhere. Thankfully, the creation graph has a resource caching system that will handle this storage for us. Second, we need to define the system required to query our mesh primitives. For most use cases, the default `vertex_buffer_system` is the best option. Third, we need to ask ourselves what this geometry will be used for. If the geometry should be visible to the ray tracing pipeline for instance. This is a design choice that should be made by the node creator. In this example, we will take ray tracing into account.

First, let us query the default `vertex_buffer_system`, if this is not available our node will not work so we can early out:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,vertex_buffer_system)}}
```

Next we will be creating the resources needed for our node. This will be a `tm_shader_constant_buffer_instance_t`, a `tm_shader_resource_binder_instance_t`, and a GPU buffer:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,create_resource)}}
```

Now that our buffer has been created; we can start populating it with our vertex data:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,vertex_data)}}
```

Finally, we need to tell the `vertex_buffer_system` which primitives are available in our mesh and how it should access them. This is what the constant buffer and resource binder are for. Note that the layout for the vertex buffer system can be included from the `vertex_buffer_system.inl` file:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,buffer_system)}}
```

And now we have our triangle, we just have to unlock the resource cache again and set the bounding volume outputs:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c,unlock)}}
```

This is the full source code to define this creation graph CPU node:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_geometry_node.c)}}
```