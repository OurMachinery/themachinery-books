# Custom Import Settings

This walkthrough shows you some basics of the [Creation Graph]({{base_url}}/creation_graphs/concept.html). In this part we discuss how to use custom import settings. This part is build on top of walkthroughs: [Creation Graph Prototype]({{base_url}}/creation_graph/introduction_walkthrough/creation_graph_prototype.html) and [Texture Compression]({{base_url}}/creation_graph/introduction_walkthrough/texture_compression.html) 

> **Note:** walkthrough series makes use of the following free assets: [KhronosGroup](https://github.com/KhronosGroup)/**[glTF-Sample-Models](https://github.com/KhronosGroup/glTF-Sample-Models)**.

This tutorial will teach you:

- How add a custom Import Setting
- When creation graphs are imported from a DCC asset they make use of these settings

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/OhpIXmMgblw?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Setup

Before you can follow this tutorial you need to follow the following steps:

- Download the flight helmet asset from the git repo [Download Now](https://downgit.github.io/#/home?url=https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/FlightHelmet/glTF).

- Create a new `dcc-image-compress` creation graph such as described in [Creation Graph Prototype]({{base_url}}/creation_graph/introduction_walkthrough/creation_graph_prototype.html) and [Texture Compression]({{base_url}}/creation_graph/introduction_walkthrough/texture_compression.html) Videos / Tutorials. We will use this in this tutorial as basis.

  

## Create a Import Settings

Default settings are just an asset in the Asset browser. To create one you open the new menu with **Right Click** and than you select **New** in the context menu. There you select the **Import Settings** . This will create a new Import Settings asset in the root folder.

> **Note:** This Import setting will be used from now on as the default one for any asset that is imported in this folder. This allows you to create import settings for different folders. Remember that this means that if the engine cannot find a import setting in the current folder it will check its parent folder and so on. In case it cannot find anything it will use the default settings.

When you select the asset you can see many different things:

![](https://paper-attachments.dropbox.com/s_8A68AE93396574AC0D937BFA8CFC626D302DBC4E0617A82A7B5162043ADD88EF_1615469368165_image.png)

This tutorial will only handle the **DCC Asset - Creation Graph - Images** and the **Import - Creation Graphs - Images**

## DCC Image Creation Graph

Now we make use of the previously created `dcc-image-compress`. This creation graph enables image compression and exposed the compression settings as a public input.

{image}

Now can can change in the Import Settings the for the DCC Asset Creation Graphs: Images

![](https://www.dropbox.com/s/dtkra0xs17yxvlq/tm_tut_cg_walkthough_import_settings.png?dl=1)

We change this to our `dcc-image-compress` creation graph.

## Import Asset

Now when we import the dcc asset we can see that the textures are auto compressed when we extract all the textures from the dcc asset.

## What about importing just a texture file?

Another way of important a texture is by simply drag and drop a png or other texture file into the asset browser. Important to note here is that images that are imported and **not part of a dcc asset** do not use the same creation graph. Those imports make use o the **Import - Creation Graphs**. The major difference between the graphs is that the previously used creation graph:

{image}

Extracts its texture from a dcc asset while in case of importing a texture directly we read the data from disc.

{image}

We just apply the same technique as we already did in the `dcc-image-compress`. 

### Create the Import Image Compress creation graph

1. We create a new creation graph in the asset browser
2. We base it on the `image-import` creation graph
3. We add the `Compress Image` node between the `Input Image Archive` and the `Image->GPU Image` node
4. We also expose the compression settings as new input and also set it via the property panel to public

The graph should look like this:

![](https://www.dropbox.com/s/xnpj45zjxkw5kez/tm_tut_cgw_image_import_cg.png?dl=1)

### Apply the correct settings to the Import Settings

What is left to do is change the creation graph for Import Images to our new `import-image-compress` creation graph in the Import Settings.
