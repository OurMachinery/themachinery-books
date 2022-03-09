# Creating custom CPU nodes

In this tutorial we will create a simple CPU node for the [*Creation Graph*]({{base_url}}/creation_graphs/concept.html). The definition for these nodes is based on the Entity Graph Nodes, so there is some overlap. For this example we will create a node that generates a random `uint32_t` node with a settable maximum. To learn the difference between CPU and GPU nodes, check out [*Node Types*]({{base_url}}/creation_graphs/node_types.html).

![](https://www.dropbox.com/s/04s5rzhmg9iwz68/tut_creation_graph_cpu_random.png?dl=1)

Let’s first create the code for this node. This function will be called by the creation graph every time it needs to evaluate the node. Our only input to this function is the context of the creation graph. The first thing we will do is read our input from the context. We can query wires from the `tm_creation_graph_interpreter_api` using the `read_wire()` function. If this wire is not connected (or set directly) we early out with an error. After this, we start writing to our output wire. Note that this uses a very similar syntax, expect that we write to a pre-allocated pointer.

> **Note** that the indices of these wires is relative to the way they are defined. Our input wire is defined first so its index is 0. The output wire is defined second so it gets the index 1.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_cpu_nodes.c,custom_cpu_node_fn)}}
```

We need to register this node to the creation graph API. This is done through the creation graph node interface. We define the general information to the node like its `name`, `display_name` and I/O connectors (wires), and the actual function to run:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_cpu_nodes.c,custom_cpu_node_node)}}
// register in the load function
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_cpu_nodes.c,custom_cpu_node_register)}}
```

This is the full code to define this creation graph CPU node:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/creation_graph/custom_cpu_nodes.c)}}
```