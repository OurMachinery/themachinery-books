# How to create prototypes

This walkthrough shows you how to create a Prototype.

## New Prototype based on a new Asset

The Machinery supports three types of assets as prototypes:

- Creation Graphs
- Entity Graphs
- Entities

You can create such prototypes via the Asset Browser **Right-Click -> New -> Creation Graph, Entity Graph, Entity.**

This will add a new asset to your project. They can function as Prototypes for the specified type. Any changes applied to them will be applied to all its instances.

## Entity Asset Prototype: Drag and Drop

You can create a Prototype from an Entity by simply drag and drop it from the Entity Tree View into the Asset Browser.

![](https://www.dropbox.com/s/erc3f4wqjoy5djt/tm_tut_prototype_create_drag.png?dl=1)

This will create a new asset of the file extension `.entity`, and the Editor will replace the Entity in the Entity Tree with an instantiated version of this Prototype.



## Entity Asset Prototype: Create Prototype from Entity

You can also create a Prototype by using the context menu in the Entity Tree View on the Entity you want to turn into a Prototype.

![](https://www.dropbox.com/s/ys17wsljt82s2me/tm_tut_prototype_create_context.png?dl=1)



## Entity Graph and Creation Graph Prototypes via subgraphs

You can turn a subgraph into a prototype by simply using the subgraph node's context menu and select Create Subgraph prototype. This will create a Subgraph Prototype Asset (.entity_graph) in your Asset Browser. When you open it you are opening the instanced version. Any change to this version will not be shared across all other versions! Only changes made to the Prototype will propagate to all changes! To open a prototype, you can use the "Open Prototype" Button.

![](https://www.dropbox.com/s/kstww1jbo3dpvwj/tm_guide_entity_graph_create_subgraph_prototype.gif?dl=1)



## Composing Prototype of other prototypes

The prototype system allows you to construct a prototype that is composed of other prototypes. This ability gives you the option to create Prototype Variants as well.