# Creating custom geometry nodes

In this tutorial we well be creating a simple CPU node for the creation graph that creates a simple mesh to be used in rendering nodes. This tutorial expects some basic knowledge of the creation graph and node creation. it is recommended to read `Creating custom CPU nodes` before reading this.

![](https://paper-attachments.dropbox.com/s_04714ABB7614AA7E464946A69D4D155B5E36439454460DD779DF6945F603E630_1634385638581_Screenshot_2.png)


The main output of this node will be a `tm_gpu_geometry_t` and a `tm_renderer_draw_call_info_t`. Together these will make out `GPU Geometry` output. Additionally we will be outputting a bounding box for the triangle that can be used for culling and other calculations. But before we can populate those we’ll need to consider the vertex format of our mesh. For this example this will be a simple position, normal, and color per vertex.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/creation_graph/custom_geometry_node.c}}
```

The `tm_renderer_draw_call_info_t` is constant for our example so we can populate that like follows. Note that this node doesn’t create an index buffer and thusly uses `TM_RENDERER_DRAW_TYPE_NON_INDEXED`.

```c
const uint32_t geometry_wire_size = sizeof(tm_gpu_geometry_t) + sizeof(tm_renderer_draw_call_info_t);
uint8_t *geometry_wire_data = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[0], TM_TYPE_HASH__GPU_GEOMETRY, 1, geometry_wire_size);
memset(geometry_wire_data, 0, geometry_wire_size);

tm_renderer_draw_call_info_t *draw_call = (tm_renderer_draw_call_info_t *)(geometry_wire_data + sizeof(tm_gpu_geometry_t));
*draw_call = (tm_renderer_draw_call_info_t) {
	.primitive_type = TM_RENDERER_PRIMITIVE_TYPE_TRIANGLE_LIST,
	.draw_type = TM_RENDERER_DRAW_TYPE_NON_INDEXED,
	.non_indexed.num_vertices = 3,
	.non_indexed.num_instances = 1
};
```

Creating the geometry for this node requires us to take several considerations. Firstly we will need to store the vertex buffer, constant buffer, and resource binder somewhere. Thankfully the creation graph has a resource caching system that will handle this storage for us. Secondly we need to define the system required to query our mesh primitives. For most use cases the default `vertex_buffer_system` is the best option. Thirdly we need to ask ourselves what this geometry will be used for. If the geometry should be visible to the ray tracing pipeline for instance. This is a design choice that should be made by the node creator but, in this example we will take ray tracing into account.

First let us query the default `vertex_buffer_system`, if this is not available our node will not work so we can early out.

```c
gpu_geometry->vfetch_system = tm_shader_repository_api->lookup_system(context->shader_repository, TM_STATIC_HASH("vertex_buffer_system", 0x6289889fc7c40280ULL));
```

Next we will be creating the resources needed for our node. This will be a `tm_shader_constant_buffer_instance_t`, `tm_shader_resource_binder_instance_t`, and a GPU buffer.

```c
tm_creation_graph_node_cache_t *node_cache = tm_creation_graph_api->lock_resource_cache(context->tt, ctx->graph_id, ctx->node_id);
tm_shader_io_o *io = tm_shader_api->system_io(gpu_geometry->vfetch_system);

tm_shader_constant_buffer_instance_t *cbuffer = (tm_shader_constant_buffer_instance_t *)node_cache->scratch_pad;
tm_shader_resource_binder_instance_t *rbinder = (tm_shader_resource_binder_instance_t *)node_cache->scratch_pad + sizeof(tm_shader_constant_buffer_instance_t);

if (!cbuffer->instance_id)
	tm_shader_api->create_constant_buffer_instances(io, 1, cbuffer);
if (!rbinder->instance_id)
	tm_shader_api->create_resource_binder_instances(io, 1, rbinder);

gpu_geometry->vfetch_system_cbuffer = cbuffer->instance_id;
gpu_geometry->vfetch_system_rbinder = rbinder->instance_id;

if (!node_cache->handles[0].resource) {
	const tm_renderer_buffer_desc_t vbuf_desc = {
		.size = 3 * sizeof(tm_triangle_vertex_t),
		.usage_flags = TM_RENDERER_BUFFER_USAGE_STORAGE | TM_RENDERER_BUFFER_USAGE_ACCELERATION_STRUCTURE,
		.debug_tag = "geometry__triangle_vbuf"
	};

	tm_triangle_vertex_t *vbuf_data;
	node_cache->handles[0] = tm_renderer_api->tm_renderer_resource_command_buffer_api->map_create_buffer(res_buf, &vbuf_desc, TM_RENDERER_DEVICE_AFFINITY_MASK_ALL, 0, (void **)&vbuf_data);
```

Now that our buffer has been created; we can start populating it with our vertex data.

```c
vbuf_data[0] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { 0.0f, 1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 1.0f, 0.0f, 0.0f } };
vbuf_data[2] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { 1.0f, -1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 0.0f, 1.0f, 0.0f } };
vbuf_data[1] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { -1.0f, -1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 0.0f, 0.0f, 1.0f } };
```

Finally we need to tell the `vertex_buffer_system` which primitives are available in our mesh and how it should access this. This is what the constant buffer and resource binder are for. Note that the layout for the vertex buffer system can be includes using the `vertex_buffer_system.inl` file.

```c
tm_shader_vertex_buffer_system_t constants = { 0 };
constants.vertex_buffer_header[0] |= (1 << TM_VERTEX_SEMANTIC_POSITION) | (1 << TM_VERTEX_SEMANTIC_NORMAL) | (1 << TM_VERTEX_SEMANTIC_COLOR0);

uint32_t *offsets = (uint32_t *)&constants.vertex_buffer_offsets;
offsets[TM_VERTEX_SEMANTIC_POSITION] = tm_offset_of(tm_triangle_vertex_t, pos);
offsets[TM_VERTEX_SEMANTIC_NORMAL] = tm_offset_of(tm_triangle_vertex_t, normal);
offsets[TM_VERTEX_SEMANTIC_COLOR0] = tm_offset_of(tm_triangle_vertex_t, color);

uint32_t *strides = (uint32_t *)&constants.vertex_buffer_strides;
strides[TM_VERTEX_SEMANTIC_POSITION] = sizeof(tm_triangle_vertex_t);
strides[TM_VERTEX_SEMANTIC_NORMAL] = sizeof(tm_triangle_vertex_t);
strides[TM_VERTEX_SEMANTIC_COLOR0] = sizeof(tm_triangle_vertex_t);

void *cbuf = (void *)&constants;
tm_shader_api->update_constants_raw(io, res_buf, &cbuffer->instance_id, &cbuf, 0, sizeof(tm_shader_vertex_buffer_system_t), 1);

uint32_t pos_buffer_slot, normal_buffer_slot, color_buffer_slot;
tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_position_buffer", 0x1ef08bede3820d69ULL), NULL, &pos_buffer_slot);
tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_normal_buffer", 0x781ed2624b12ebbcULL), NULL, &normal_buffer_slot);
tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_color0_buffer", 0xb808f20e2f260026ULL), NULL, &color_buffer_slot);

const tm_shader_resource_update_t res_updates[] = {
	{ .instance_id = rbinder->instance_id,
		.resource_slot = pos_buffer_slot,
		.num_resources = 1,
		.resources = node_cache->handles },
	{ .instance_id = rbinder->instance_id,
		.resource_slot = normal_buffer_slot,
		.num_resources = 1,
		.resources = node_cache->handles },
	{ .instance_id = rbinder->instance_id,
		.resource_slot = color_buffer_slot,
		.num_resources = 1,
		.resources = node_cache->handles }
};

tm_shader_api->update_resources(io, res_buf, res_updates, TM_ARRAY_COUNT(res_updates));
```

And that is our triangle made, we just have to unlock the resource cache again and set the bounding volume outputs.

```c
	tm_creation_graph_api->unlock_resource_cache(node_cache);
}

tm_vec3_t *bounds_min = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[1], TM_TT_TYPE_HASH__VEC3, 1, sizeof(tm_vec3_t));
tm_vec3_t *bounds_max = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[2], TM_TT_TYPE_HASH__VEC3, 1, sizeof(tm_vec3_t));

*bounds_min = (tm_vec3_t) { -1.0f, -1.0f, 0.0f };
*bounds_max = (tm_vec3_t) { 1.0f, 1.0f, 0.0f };
```

This is the full source code to define this creation graph CPU node.

```c
struct tm_creation_graph_interpreter_api *tm_creation_graph_interpreter_api;
struct tm_shader_api *tm_shader_api;
struct tm_shader_repository_api *tm_shader_repository_api;
struct tm_renderer_api *tm_renderer_api;

#include <foundation/api_registry.h>
#include <foundation/the_truth_types.h>
#include <foundation/macros.h>
#include <foundation/atomics.inl>

#include <plugins/creation_graph/creation_graph.h>
#include <plugins/creation_graph/geometry_nodes.h>
#include <plugins/creation_graph/creation_graph_node_type.h>
#include <plugins/creation_graph/creation_graph_interpreter.h>
#include <plugins/renderer/renderer.h>
#include <plugins/renderer/commands.h>
#include <plugins/renderer/resources.h>
#include <plugins/renderer/render_command_buffer.h>
#include <plugins/shader_system/shader_system.h>
#include <plugins/renderer/render_backend.h>

#include <string.h>

#include <plugins/creation_graph/resource_cache_internal.inl>

typedef struct tm_triangle_vertex_t
{
	tm_vec3_t pos;
	tm_vec3_t normal;
	tm_vec3_t color;
} tm_triangle_vertex_t;

static void triangle_node__compile(tm_creation_graph_interpreter_context_t *ctx, tm_creation_graph_compile_context_t *compile_ctx)
{
	tm_creation_graph_context_t *context = *(tm_creation_graph_context_t **)tm_creation_graph_interpreter_api->read_wire(ctx->instance, TM_CREATION_GRAPH__STATIC_WIRE__CONTEXT).data;
	if (!context)
		return;

	const uint32_t geometry_wire_size = sizeof(tm_gpu_geometry_t) + sizeof(tm_renderer_draw_call_info_t);
	uint8_t *geometry_wire_data = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[0], TM_TYPE_HASH__GPU_GEOMETRY, 1, geometry_wire_size);
	memset(geometry_wire_data, 0, geometry_wire_size);

	tm_renderer_draw_call_info_t *draw_call = (tm_renderer_draw_call_info_t *)(geometry_wire_data + sizeof(tm_gpu_geometry_t));
	*draw_call = (tm_renderer_draw_call_info_t) {
		.primitive_type = TM_RENDERER_PRIMITIVE_TYPE_TRIANGLE_LIST,
		.draw_type = TM_RENDERER_DRAW_TYPE_NON_INDEXED,
		.non_indexed.num_vertices = 3,
		.non_indexed.num_instances = 1
	};

	tm_gpu_geometry_t *gpu_geometry = (tm_gpu_geometry_t *)geometry_wire_data;
	gpu_geometry->vfetch_system = tm_shader_repository_api->lookup_system(context->shader_repository, TM_STATIC_HASH("vertex_buffer_system", 0x6289889fc7c40280ULL));
	if (gpu_geometry->vfetch_system) {
#include <the_machinery/shaders/vertex_buffer_system.inl>

		tm_renderer_resource_command_buffer_o *res_buf = context->res_buf[TM_CREATION_GRAPH_RESOURCE_BUFFERS__PRE_CMD];
		tm_creation_graph_node_cache_t *node_cache = tm_creation_graph_api->lock_resource_cache(context->tt, ctx->graph_id, ctx->node_id);
		tm_shader_io_o *io = tm_shader_api->system_io(gpu_geometry->vfetch_system);

		tm_shader_constant_buffer_instance_t *cbuffer = (tm_shader_constant_buffer_instance_t *)node_cache->scratch_pad;
		tm_shader_resource_binder_instance_t *rbinder = (tm_shader_resource_binder_instance_t *)node_cache->scratch_pad + sizeof(tm_shader_constant_buffer_instance_t);

		if (!cbuffer->instance_id)
			tm_shader_api->create_constant_buffer_instances(io, 1, cbuffer);
		if (!rbinder->instance_id)
			tm_shader_api->create_resource_binder_instances(io, 1, rbinder);

		gpu_geometry->vfetch_system_cbuffer = cbuffer->instance_id;
		gpu_geometry->vfetch_system_rbinder = rbinder->instance_id;

		if (!node_cache->handles[0].resource) {
			const tm_renderer_buffer_desc_t vbuf_desc = {
				.size = 3 * sizeof(tm_triangle_vertex_t),
				.usage_flags = TM_RENDERER_BUFFER_USAGE_STORAGE | TM_RENDERER_BUFFER_USAGE_ACCELERATION_STRUCTURE,
				.debug_tag = "geometry__triangle_vbuf"
			};

			tm_triangle_vertex_t *vbuf_data;
			node_cache->handles[0] = tm_renderer_api->tm_renderer_resource_command_buffer_api->map_create_buffer(res_buf, &vbuf_desc, TM_RENDERER_DEVICE_AFFINITY_MASK_ALL, 0, (void **)&vbuf_data);

			vbuf_data[0] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { 0.0f, 1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 1.0f, 0.0f, 0.0f } };
			vbuf_data[2] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { 1.0f, -1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 0.0f, 1.0f, 0.0f } };
			vbuf_data[1] = (tm_triangle_vertex_t) { .pos = (tm_vec3_t) { -1.0f, -1.0f, 0.0f }, .normal = (tm_vec3_t) { 0.0f, 0.0f, 1.0f }, .color = (tm_vec3_t) { 0.0f, 0.0f, 1.0f } };

			tm_shader_vertex_buffer_system_t constants = { 0 };
			constants.vertex_buffer_header[0] |= (1 << TM_VERTEX_SEMANTIC_POSITION) | (1 << TM_VERTEX_SEMANTIC_NORMAL) | (1 << TM_VERTEX_SEMANTIC_COLOR0);

			uint32_t *offsets = (uint32_t *)&constants.vertex_buffer_offsets;
			offsets[TM_VERTEX_SEMANTIC_POSITION] = tm_offset_of(tm_triangle_vertex_t, pos);
			offsets[TM_VERTEX_SEMANTIC_NORMAL] = tm_offset_of(tm_triangle_vertex_t, normal);
			offsets[TM_VERTEX_SEMANTIC_COLOR0] = tm_offset_of(tm_triangle_vertex_t, color);

			uint32_t *strides = (uint32_t *)&constants.vertex_buffer_strides;
			strides[TM_VERTEX_SEMANTIC_POSITION] = sizeof(tm_triangle_vertex_t);
			strides[TM_VERTEX_SEMANTIC_NORMAL] = sizeof(tm_triangle_vertex_t);
			strides[TM_VERTEX_SEMANTIC_COLOR0] = sizeof(tm_triangle_vertex_t);

			void *cbuf = (void *)&constants;
			tm_shader_api->update_constants_raw(io, res_buf, &cbuffer->instance_id, &cbuf, 0, sizeof(tm_shader_vertex_buffer_system_t), 1);

			uint32_t pos_buffer_slot, normal_buffer_slot, color_buffer_slot;
			tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_position_buffer", 0x1ef08bede3820d69ULL), NULL, &pos_buffer_slot);
			tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_normal_buffer", 0x781ed2624b12ebbcULL), NULL, &normal_buffer_slot);
			tm_shader_api->lookup_resource(io, TM_STATIC_HASH("vertex_buffer_color0_buffer", 0xb808f20e2f260026ULL), NULL, &color_buffer_slot);

			const tm_shader_resource_update_t res_updates[] = {
				{ .instance_id = rbinder->instance_id,
					.resource_slot = pos_buffer_slot,
					.num_resources = 1,
					.resources = node_cache->handles },
				{ .instance_id = rbinder->instance_id,
					.resource_slot = normal_buffer_slot,
					.num_resources = 1,
					.resources = node_cache->handles },
				{ .instance_id = rbinder->instance_id,
					.resource_slot = color_buffer_slot,
					.num_resources = 1,
					.resources = node_cache->handles }
			};

			tm_shader_api->update_resources(io, res_buf, res_updates, TM_ARRAY_COUNT(res_updates));
		}

		tm_creation_graph_api->unlock_resource_cache(node_cache);
	}

	tm_vec3_t *bounds_min = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[1], TM_TT_TYPE_HASH__VEC3, 1, sizeof(tm_vec3_t));
	tm_vec3_t *bounds_max = tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[2], TM_TT_TYPE_HASH__VEC3, 1, sizeof(tm_vec3_t));

	*bounds_min = (tm_vec3_t) { -1.0f, -1.0f, 0.0f };
	*bounds_max = (tm_vec3_t) { 1.0f, 1.0f, 0.0f };
}

static tm_creation_graph_node_type_i triangle_node = {
	.name = "tm_geometry_triangle",
	.display_name = "Triangle",
	.category = "Geometry",
	.static_connectors.num_out = 3,
	.static_connectors.out = {
		{ .name = "gpu_geometry", .display_name = "GPU Geometry", .type_hash = TM_TYPE_HASH__GPU_GEOMETRY },
		{ .name = "bounds_min", .display_name = "Bounds Min", .type_hash = TM_TT_TYPE_HASH__VEC3, .optional = true },
		{ .name = "bounds_max", .display_name = "Bounds Max", .type_hash = TM_TT_TYPE_HASH__VEC3, .optional = true }
	},
	.compile = triangle_node__compile
};

TM_DLL_EXPORT void load_triangle_geometry(struct tm_api_registry_api *reg, bool load)
{
	tm_creation_graph_interpreter_api = tm_get_api(reg, tm_creation_graph_interpreter_api);
	tm_shader_api = tm_get_api(reg, tm_shader_api);
	tm_shader_repository_api = tm_get_api(reg, tm_shader_repository_api);
	tm_renderer_api = tm_get_api(reg, tm_renderer_api);

	tm_add_or_remove_implementation(reg, load, tm_creation_graph_node_type_i, &triangle_node);
}
```