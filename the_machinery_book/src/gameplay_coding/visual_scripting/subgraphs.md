# Subgraphs

Subgraphs are a way to organize your graph better and create smaller units. They make them easier to maintain and easy to follow. In its essence a subgraph is a graph within a graph. They are interfaced via a subgraph node. They can produce Input and Output, such as a normal node could. They can also call and react to normal Events!

## Create a subgraph

You create a new subgraph by simply selecting all nodes that shall be part of the subgraph. After that, click on them with the right mouse and select Create Subgraph from the context menu**.** The subgraph will replace the selected nodes. You can change its label in the property view. By simply double click you open the subgraph.

![](https://www.dropbox.com/s/k688sg41w5507mn/tm_guide_entity_graph_create_subgraph.gif?dl=1)

## Subgraph Inputs

A subgraph can have inputs and outputs. You can add them to them the same way as for a normal Graph. But you can also just connect the needed wires with the subgraph node, as the following image shows:

![](https://www.dropbox.com/s/18b2z2f1ed80ex6/tm_guide_entity_graph_create_subgraph_input_output.gif?dl=1)



## Subgraph Prototypes

The Machinery's  **Prototype** system allows you to create, configure, and store an Entity/Creation Graph complete with all its subgraphs, input/output nodes as a reusable Entity / Creation Graph Asset. 

> **Note:** Since the Entity Graph and the Creation Graph are conceptually similar the same aspects apply to them both! However this document will only focus on the Entity Graph.

This Asset acts as a template from which you can create new Prototype instances in other Entity Graphs/Creation Graphs. Any edits that you make to the Asset are automatically reflected in the instances of that Graph, allowing you to easily make broad changes across your whole Project without having to repeatedly make the same edit to every copy of the Asset.

> **Note:** This does not mean all Prototype instances are identical. You can override individually and add/remove nodes from them, depending on your need!



### Create a subgraph Prototype

You can turn a subgraph into a prototype by simply using the context menu of the subgraph node and selecting Create Subgraph prototype. This will create a Subgraph Prototype Asset (`.entity_graph`) in your Asset Browser. When you open it you are opening the instanced version. Any change to this version will not be shared across all other versions! Only changes made to the prototype will propagate to all changes! To open a prototype you can use the "Open Prototype" Button. 

![](https://www.dropbox.com/s/kstww1jbo3dpvwj/tm_guide_entity_graph_create_subgraph_prototype.gif?dl=1)



