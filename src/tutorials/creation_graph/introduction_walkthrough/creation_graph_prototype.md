# Creation Graph Prototypes

This walkthrough shows you some basics of the [Creation Graph]({{base_url}}/creation_graphs/concept.html). In this part we discuss creation graph prototypes. To read more in general about the prototype system please checkout the following [Guide: Prototypes]({{base_url}}editing_workflows/prototype_workflow/index.html)

> **Note:** The walkthrough series makes use of the following free assets: [KhronosGroup](https://github.com/KhronosGroup)/**[glTF-Sample-Models](https://github.com/KhronosGroup/glTF-Sample-Models)**.

This tutorial will teach you:

- How to create Creation Graph prototypes
- How to apply them to multiple assets
- How to add extra input

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/y5Pylqxc0UE?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>



## Setup

We could do this by opening all textures and following the steps described in the [Simple Texture Compression Walkthrough]({{base_url}}/tutorials/creation_graph/introduction_walkthrough/texture_compression.html) but this would be a time consuming and error prone job. It would be easier to just create one prototype for all.

## Adding texture compression to all textures in the project

### Creating a Creation Graph Prototype

There are 2 effective ways of doing this:

1. Change the prototype of all dcc images use: `core/creation_graphs/dcc-image`

We open this prototype and apply all our changes described in  [Simple Texture Compression Walkthrough]({{base_url}}/tutorials/creation_graph/introduction_walkthrough/texture_compression.html). Changes to the prototype will propagate to all creation graph instances of this prototype.



2. Create a new creation graph and base it on `core/creation_graphs/dcc-image`

In this alternative approach we create with **Right Click** in the asset browser and then **New -> Creation Graph** a new creation graph. This graph is a empty graph. When we select the newly created asset we can chose in the property view tab the prototype of the asset.

{image}

In this selection we search for `dcc-image` and base (inherit) our new creation graph on the existing creation graph. After this we can modify this graph as described in the [Simple Texture Compression Walkthrough]({{base_url}}/tutorials/creation_graph/introduction_walkthrough/texture_compression.html).

### Applying the new prototype to all texture assets

Now we select all assets in the asset browser and change their creation graph to point to our newly creation creation graph

{image}



### Expose compression settings to the outside world

Now one problem is left it is that some of these are normal maps and for those you want different compression settings. The fix for this is to expose the Compression Node settings to the outside world. We open our newly creation creation graph connect the compression settings of the compression node with the input connector of the Input node. The original default value stays the default value of our graph Do not forget to mark them as public in the input node properties.

{image}

When this is done you can see the exposed settings when ever you select any asset in the asset browser.

{image}

What ever you change here will be passed to the compression node. This makes sure that normal maps can be treated how they are supposed to.