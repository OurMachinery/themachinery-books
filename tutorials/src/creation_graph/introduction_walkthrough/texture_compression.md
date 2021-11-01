# Texture Compression

This walkthrough shows you some basics of the [Creation Graph]({{the_machinery_book}}/creation_graphs/concept.html). In this part we discuss texture compression.

This tutorial will teach you:

- How to compress a texture
- What differentiates a creation graph from each other.

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/49eF0O5OAbY?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

> This walkthrough series makes use of the following free assets: [KhronosGroup](https://github.com/KhronosGroup)/**[glTF-Sample-Models](https://github.com/KhronosGroup/glTF-Sample-Models)**.



After we have downloaded and extracted all parts of the dcc asset as described in [Import and rigging tutorial](https://www.youtube.com/watch?v=loaYaeSl-_g&t=20s) or you follow this Guide [Import assets](https://ourmachinery.github.io/themachinery-books/the_machinery_book/editing_workflows/import_assets.html#import-assets). We set the goal to compress textures.



## How do we identify uncompressed images?

When we select a texture in the Asset Browser, lets select the leather of the helmet.

{image}

In the preview tab we can see that this texture is uncompressed indicated by the text line in the bottom of the preview.

{image}

## How do we compress the texture?

We double click the selected texture and open its creation graph. This will open the instanced version of the core `dcc_texture`creation graph. This creation graph looks as following:

{image}

### Dissection

Let us dissect the graph step by step:

| Input Node      |
| --------------- |
| DCC Asset Image |
| Image Settings  |

The Input node takes a `dcc asset image` this is a data container that contains the raw image data within the dcc asset. This raw data needs to be translated to a GPU image with the next node.

| DCC Images      |
| --------------- |
| DCC Asset Image |
| GPU Image       |

After this translation we can make use of the `Import Settings` to filter the Image with the `Filter Image`. This node filters for example mipmap.

| Filter Image |
| ------------ |
| Settings     |
| Image        |
| GPU Image    |

The output is a modified GPU Image which we pass to the `Image Output` node. 

### How to Distinguish between creation graphs and creation graph.

The output nodes define the types of the creation graph. In this particular case the creation graph represents a texture now.



### Add the compression node

We are using the `crunch` library for our image compression node. We can just press space and search for the "Compression Node" and add it to the graph. Since we are working in an Instance of the core graph we can modify this graph and the results will not change the prototype. 

| Compression Node   |
| ------------------ |
| Image              |
| GPU Image          |
| Input Colour Space |
| Output Format      |
| Release GPU Input  |

This node outputs an Image that is compressed and we can then connect this node to the Image Output node. Important to remember is that we need to remove the connection from the output node to the image filter node and remove the original connection. 

{image}

If we now investigate the image in the asset browser we can see that the texture is compressed.

{image}
