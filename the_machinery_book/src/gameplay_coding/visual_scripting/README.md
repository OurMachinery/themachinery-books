{{#include ../../editing_workflows/visual-scripting.md:0:8}}

## Basic Concepts

### How to use the Entity Graph?

You need to add a Graph Component to an Entity of your choice. 

![](https://www.dropbox.com/s/29u0c1gsu0vjghg/tm_guide_entity_graph_add_component.png?dl=1)

After that, you have two ways of opening the Graph:

- Double Click the Graph Component

- Click in the Property View on Edit

![](https://www.dropbox.com/s/p1hkay3ouhezbmh/tm_guide_entity_graph_open.gif?dl=1)

Now the Graph Editor Opens and you can start adding nodes via:

- **Right Click -> Add Node**
- **Press Space**

### Execution

The Entity Graph is an event-driven Visual Scripting language. This means everything happens after an event is triggered! By default, the Engine comes with the following built-in Events:

| Name            | Description |                                                              |
| --------------- | ----------- | ------------------------------------------------------------ |
| Init Event      | Is called when the component is added to the Entity. | <img src="https://www.dropbox.com/s/6cov2jbv72iy455/tm_guide_entity_graph_init.png?dl=1" width="277" height="120"> |
| Reload Event    | Is called when the component is reloaded from the truth. | <img src="https://www.dropbox.com/s/zixoinmbta73tir/tm_guide_entity_graph_reload.png?dl=1" width="277" height="120"> |
| Tick Event      | Is called every frame. | <img src="https://www.dropbox.com/s/1t7hwmu37wr4aua/tm_guide_entity_graph_tick.png?dl=1" width="277" height="120">  |
| Terminate Event | Is called before the component is removed from the entity. | <img src="https://www.dropbox.com/s/nx3tehccedx7qic/tm_guide_entity_graph_terminate.png?dl=1" width="277" height="120">  |
| Custom Event | Is called when the named event<br> is triggered with either a "Trigger Event"<br> node or from the outside with "Trigger Remote Event" | <img src="https://www.dropbox.com/s/ngv3k25u02k8iq6/tm_guide_entity_graph_create_custom_event.png?dl=1" width="277" height="120">  |
| Trigger Event | Triggers an event. | <img src="https://www.dropbox.com/s/tqyg6scxjcsk3vi/tm_guide_entity_graph_trigger.png?dl=1" width="277" height="120">  |
| Trigger Remote Event | Triggeres an event on a remote Entity | <img src="https://www.dropbox.com/s/jrnapuuq93d0kx8/tm_guide_entity_graph_trigger_remote.png?dl=1" width="277" height="120">  |
| UI Tick | Is ticked every frame regardless if the game is paused or not! | <img src="https://www.dropbox.com/s/6ejvwvc5yndpo87/tm_guide_entity_graph_ui_tick.png?dl=1" width="277" height="120">  |

### Anatomy

There are six types of nodes:

| Type        | Function                                                     |
| ----------- | ------------------------------------------------------------ |
| Event Node  | Starting point of the Execution                              |
| Query Node  | Query nodes are triggered  automatically when their output is requested. Nodes that aren't query nodes need to be triggered. Therefore they are "Pure" and do not modify data! |
| Nodes       | Normal nodes that have an Event input, hence they might modify the data and produce an output or mutate the graphs state! |
| Subgraphs   | Graphs within a Graph! Allow you to organize your graph into smaller units. They can also be reused if saved as Subgraph Prototype. |
| Input Node  | Accepts Input from the Outside world and makes it available to the graph. Mainly used for communication between graphs and subgraphs. |
| Output Node | Accepts Output and passes it to the Outside world and makes it available to a parent graph. Mainly used for communication between graphs and subgraphs. |



Moreover, the Visual Scripting language knows two different types of wires:

- **Event Wires** They regulate the execution flow.
- **Data Wires** Transport the data from node to node!

![](https://www.dropbox.com/s/i95s1frdzhcsev1/tm_guide_entity_graph_wire_types.png?dl=1)



## Inputs

Graphs can have inputs. They can be used to allow the user of your graph to pass data from the outside (e.g. the Editor) to the graph. This happens via the Input Nodes. In the General Graph settings you can add Inputs from the outside world.

### Adding a Public Input

1. You click on the Settings button which opens the Graphs Settings

![image](https://www.dropbox.com/s/na7s582ljyxmnnf/tm_guide_entity_graph_settings.png?dl=1)

2. You expand the Input Accordion and press "Add"

   ![](https://www.dropbox.com/s/hv7qiqqhy4gbauw/tm_guide_entity_graph_add_input.png?dl=1)

   

3. This will add a new Input to your graph! There you have a few options. 

   ![](https://www.dropbox.com/s/s50hbn0sqhixlx3/tm_guide_entity_graph_input_node_settings.png?dl=1)

To make your node public just check the publicly accessible from another graph or from the Editor check the Public checkbox

![](https://www.dropbox.com/s/1m243i24lhwbosw/tm_guide_entity_graph_input_node_make_public.png?dl=1)

If you now select the Graph Component of your Entity you will be able to change the value:

![](https://www.dropbox.com/s/ojite1pycbs75pq/tm_guide_entity_graph_input_node_public.png?dl=1)

This can be a nice way to customize behaviour of your graph and entity!

4. Add an Input node to your graph. There you have access to the data.

   ![](https://www.dropbox.com/s/l20w7d0utoet9ti/tm_guide_entity_graph_input_node.png?dl=1)

   The Input Node also allows you to access the settings. Hover over the name of the Input and a Settings option becomes available. 

   ![](https://www.dropbox.com/s/wrg5hk7lbx0l1rs/tm_guide_entity_graph_input_node_on_settings.png?dl=1)

### Variables

You can store data within your Graph! The Set / Get Variable nodes are the way to go. They give you access to this function. You can also access variables from distance Entities by using the Set / Get Remote Variable nodes.

![](https://www.dropbox.com/s/dgddk1xmw16dlp1/tm_guide_entity_graph_create_remote_variable.png?dl=1)



### Branches and loops

The Language comes with built-in support for branches, the If node. The Language supports multiple bool operators to compare values.

Besides, you have two nodes for loops:

- The Grid node
- The For node

*The Grid node for example:*

![](https://www.dropbox.com/s/9fawc756lyf0k3h/tm_guide_entity_graph_loop.png?dl=1)



### Subgraphs

You can organize your code into smaller reusable units and combine nodes as a subgraph! Using subgraphs makes your Graph more user-friendly, and it will look less like spaghetti. You can store your subgraph as a `.entity_graph` asset in your asset browser and allow it to be reused across your project! Which enables you to have maximal flexibility! 



## What is next?

In the next chapter you will learn more about Subgraphs and the Debugger! In case you want to provide your own Nodes check out this tutorial [Extend the Entity Graph]({{base_url}}gameplay_coding/extend_the_entity_graph.html)
