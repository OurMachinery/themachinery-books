## Entity Graphs

The *Entity Graph* implements a visual scripting language based on nodes and connections. To use
it, right-click on an entity to add a Graph Component and then double click on the Graph Component
to open it in the Graph Editor:

![Graph editor.](https://www.dropbox.com/s/ssasbp5sb0vq7gy/graph-editor.png?dl=1)

The visual scripting language uses *Events* to tick the execution of nodes. For example, the
*Tick Event* node will trigger its out connector whenever the application ticks its frame. Connect
its output event connector to another node to run that node during the application's update.

Nodes that just fetch data and don't have any side-effects are considered "pure". They don't have
any event connectors and will run automatically whenever their data is needed by one of the non-pure
nodes. Connect the data connectors with wires to pass data between nodes.

In addition to connecting wires, you can also edit input data on the nodes directly. Click a node
to select it and edit its input data in the properties.

There are a lot of different nodes in the system and I will not attempt to describe all of them.
Instead, here is a simple example that adds a super simple animation to an entity using the graph
component:

<iframe width="560" height="315" src="https://www.youtube.com/embed/3DupUNK9GNc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## What is next?

For more information go and checkout the [Gameplay Coding / Visual Scripting Chapter]({{the_machinery_book}}/gameplay_coding/visual_scripting/index.html)

For more examples, check out the `pong` and `animation` projects in the samples.

