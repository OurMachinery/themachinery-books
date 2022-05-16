# Creating Prototype Assets

This walkthrough shows you how to create *Prototype Assets*.

*Prototypes* act as "templates" or "prefabs" for other assets. When you instantiate a prototype, the instance will inherit all the properties of the prototype unless you specifically override them.

In The Machinery there is no distinction between "prototype assets" and "ordinary assets". Any asset can be used as a prototype for other assets. The prototype system is also hierarchical. I.e., prototypes may themselves have prototypes. This lets you mix and match assets in lots of interesting ways.

## Create a Prototype as a New Asset

In The Machinery, the assets most commonly used as prototypes are:

- Entities
- Entity Graphs
- Creation Graphs

Since prototypes are just an ordinary assets, you can create an empty prototype, by creating an asset of the desired type in the Asset Browser: **Right Click → New → Entity/Entity Graph/Creation Graph**. 

This will add a new asset to your project. Any changes made to the asset will be applied to all instances of the prototype.

## Entity Prototype: Drag and Drop

You can create a Prototype from an Entity by simply dragging and dropping it from the Entity Tree into the Asset Browser.

![](https://www.dropbox.com/s/erc3f4wqjoy5djt/tm_tut_prototype_create_drag.png?raw=1)

This creates a new asset with the file extension `.entity`. It also replaces the entity in the Entity Tree with an instance of the newly created prototype.

## Entity Prototype: Create Prototype from Entity

You can also create a prototype by using the context menu in the Entity Tree View on the Entity you want to turn into a Prototype:

![](https://www.dropbox.com/s/ys17wsljt82s2me/tm_tut_prototype_create_context.png?raw=1)



## Graph Prototypes from Subgraphs

You can turn a Subgraph into a prototype by choosing **Create Subgraph Prototype** in the Subgraph node's context menu. This creates a Subgraph Prototype Asset (`.entity_graph`) in your Asset Browser. It will also change the Subgraph to become an instance of the newly created prototype. If you open the Subgraph node at this point all the nodes will be grayed out. This shows that they are inherited from the prototype. Any changes you make there will be local to that instance.

To make a change that propagates to all instances of the prototype, open the prototype in the asset browser, or by using the **Open Prototype** button in the Properties view of the Subgraph node.

![](https://www.dropbox.com/s/kstww1jbo3dpvwj/tm_guide_entity_graph_create_subgraph_prototype.gif?raw=1)


