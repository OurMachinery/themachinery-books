# Instantiating Prototypes

How you create prototype instances depend on what kind of prototype you want to instance.



## Entity Prototypes

To create an instance of an entity prototype, you can simply drag an drop the entity from the Asset Browser into the Entity Tree or the Scene Tab:

![](https://www.dropbox.com/s/hxrfnyppjfrzrjg/tm_tut_prototype_entity_drag.png?raw=1)

You can also use the context menu in the Entity Tree to replace any entity with an instantiated asset:

![](https://www.dropbox.com/s/7977n6966p9qhbh/tm_tut_prototype_replace_asset.png?raw=1)

At runtime, you can create instances of an entity asset by spawning them from the Entity Graph:

![](https://www.dropbox.com/s/n5h5art3g8ws53y/tm_tut_prototype_spawn_entity.png?raw=1)



## Subgraph Prototypes

You can add an instance of a Subgraph by dropping the `.graph` asset from the Asset Browser into the Graph editor.

Note that the dropped graph must be of the same type as the graph you are editing. I.e. Creation Graph Subgraphs can only be used in Creation Graphs, Entity Graph Subgraphs can only be used in Entity Graphs.

![](https://www.dropbox.com/s/zf0vgfw6jm3yj09/tm_tut_prototype_subgraph_drag.png?raw=1)

Another way of creating an instance of a Subgraph is to create an empty Subgraph node in the Graph and then picking a prototype for it in the Properties view:

![](https://www.dropbox.com/s/cdmcftplipgysx5/tm_tut_prototype_subgraph_node.png?raw=1)



## Creation Graph Prototypes

The Render Component and other components that make use of Creation Graphs typically let you specify the prototype to use for the Creation Graph in the Properties View:

![](https://www.dropbox.com/s/duklb4r264uqrt5/tm_tut_prototype_creation_graph.png?raw=1)

The **Edit** button in this view lets you open the specific Creation Graph instance used by this component for editing.