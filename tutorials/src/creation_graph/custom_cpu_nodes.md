# Creating custom CPU nodes

In this tutorial we will create a simple CPU node for the [*Creation Graph*]({{the_machinery_book}}/creation_graphs/concept.html). The definition for these nodes is based on the entity graph nodes, so there is some overlap. The goal for our example node is a random `uint32_t` node with a settable maximum. To learn the difference between CPU and GPU nodes, check out [*Node Types*]({{the_machinery_book}}/creation_graphs/node_types.html).

![](https://www.dropbox.com/s/04s5rzhmg9iwz68/tut_creation_graph_cpu_random.png?dl=1)

Let’s first create the code for this node. This function will be called by the creation graph every time it needs to evaluate the node. Our only input to this function is the context of the creation graph. The first thing we will do is read our input from the context. We can query wires from the `tm_creation_graph_interpreter_api` using the `read_wire` function. If this wire is not connect (or set directly) we early out with an error. After this we start writing to our output wire, note that this uses a very similar syntax, expect that we write to a pre-allocated pointer.

> **Note** that the indices of these wires is relative to the way they are defined. Our input wire is defined first so its index is zero. The output wire is defined second so it gets the index one.
    
```c
static void random_node__run(tm_creation_graph_interpreter_context_t *ctx)
{
	tm_creation_graph_interpreter_wire_content_t max_wire = tm_creation_graph_interpreter_api->read_wire(ctx->instance, ctx->wires[0]);
	if (!TM_ASSERT(max_wire.n, tm_error_api->def, "Max wire was not connected to random node!"))
		return;

	uint32_t *res = (uint32_t *)tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[1], TM_TT_TYPE_HASH__UINT32_T, 1, sizeof(uint32_t));
	*res = tm_random_to_uint32_t(tm_random_api->next()) % *(uint32_t *)max_wire.data;
}
```

We need to register this node to the creation graph API. This is done through the creation graph node interface. We define the general information to the node like its `name`, `display_name` and I/O connectors (wires), and the actual function to run.

```c
static tm_creation_graph_node_type_i random_node = {
	.name = "tm_random",
	.display_name = "Random Uint",
	.static_connectors.in = {
		{ .name = "max", .display_name = "Max", .type_hash = TM_TT_TYPE_HASH__UINT32_T }
	},
	.static_connectors.num_in = 1,
	.static_connectors.out = {
		{ .name = "res", .display_name = "Result", .type_hash = TM_TT_TYPE_HASH__UINT32_T }
	},
	.static_connectors.num_out = 1,
	.run = random_node__run
};

tm_add_or_remove_implementation(reg, load, TM_CREATION_GRAPH_NODE_INTERFACE_NAME, &random_node);
```

This is the full code to define this creation graph CPU node.

```c
static struct tm_error_api *tm_error_api;
static struct tm_random_api *tm_random_api;
static struct tm_creation_graph_interpreter_api *tm_creation_graph_interpreter_api;

#include <foundation/api_registry.h>
#include <foundation/error.h>
#include <foundation/random.h>
#include <foundation/the_truth_types.h>

#include <plugins/creation_graph/creation_graph.h>
#include <plugins/creation_graph/creation_graph_interpreter.h>
#include <plugins/creation_graph/creation_graph_node_type.h>

static void random_node__run(tm_creation_graph_interpreter_context_t *ctx)
{
	tm_creation_graph_interpreter_wire_content_t max_wire = tm_creation_graph_interpreter_api->read_wire(ctx->instance, ctx->wires[0]);
	if (!TM_ASSERT(max_wire.n, tm_error_api->def, "Max wire was not connected to random node!"))
		return;

	uint32_t *res = (uint32_t *)tm_creation_graph_interpreter_api->write_wire(ctx->instance, ctx->wires[1], TM_TT_TYPE_HASH__UINT32_T, 1, sizeof(uint32_t));
	*res = tm_random_to_uint32_t(tm_random_api->next()) % *(uint32_t *)max_wire.data;
}

static tm_creation_graph_node_type_i random_node = {
	.name = "tm_random",
	.display_name = "Random Uint",
	.static_connectors.in = {
		{ .name = "max", .display_name = "Max", .type_hash = TM_TT_TYPE_HASH__UINT32_T }
	},
	.static_connectors.num_in = 1,
	.static_connectors.out = {
		{ .name = "res", .display_name = "Result", .type_hash = TM_TT_TYPE_HASH__UINT32_T }
	},
	.static_connectors.num_out = 1,
	.run = random_node__run
};

TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
	tm_error_api = reg->get(TM_ERROR_API_NAME);
	tm_random_api = reg->get(TM_RANDOM_API_NAME);
	tm_creation_graph_interpreter_api = reg->get(TM_CREATION_GRAPH_INTERPRETER_API_NAME);

	tm_add_or_remove_implementation(reg, load, TM_CREATION_GRAPH_NODE_INTERFACE_NAME, &random_node);
}
```