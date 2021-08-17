# How to instantiate Prototypes

The way on how to instantiate prototypes depends on the Prototype itself.



## Entity Asset Prototypes

For example, an Entity Asset Prototype can be drag and dropped into the Entity Tree / Scene Tab.

![](https://www.dropbox.com/s/hxrfnyppjfrzrjg/tm_tut_prototype_entity_drag.png?dl=1)

You can also replace any Entity within the currently open Entity via the context menu.

![](https://www.dropbox.com/s/7977n6966p9qhbh/tm_tut_prototype_replace_asset.png?dl=1)

You can also spawn them via the Entity Graph:

![](https://www.dropbox.com/s/n5h5art3g8ws53y/tm_tut_prototype_spawn_entity.png?dl=1)

> **Note:** This means you can compose Entity Prototypes that are fully constructed of other Prototypes.



## Subgraph Prototypes

You can add creation Graph / Entity Graph prototypes to any Graph of its type. You do this by drag and drop the Graph Asset into the Graph Editor.

![](https://www.dropbox.com/s/zf0vgfw6jm3yj09/tm_tut_prototype_subgraph_drag.png?dl=1)

If you have added a Subgraph Node, you can select a suiting graph asset via the Property View.

![](https://www.dropbox.com/s/cdmcftplipgysx5/tm_tut_prototype_subgraph_node.png?dl=1)



## Creation Graph Prototypes

Most components/assets that require a creation graph can make use of a prototype type. You do this via the Prototype field in the Properties panel.

![](https://www.dropbox.com/s/duklb4r264uqrt5/tm_tut_prototype_creation_graph.png?dl=1)