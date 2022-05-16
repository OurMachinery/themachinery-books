## The asset pipeline by Example

This section we focus on how to set up a simple entity from an imported `dcc_asset`. 

You will learn the basics about:

- What the creation graph is
- How the asset pipeline works
- How to create (rigg) an Entity from an imported asset

## Introduction

There are lots of things you might want to do to an imported asset coming from a DCC-tool. For
example, extracting images and materials into a representation that can be further tweaked by your
artists or rigging (create) an entity from the meshes present in the asset. In The Machinery, we provide full
control over how data enters the engine and what data-processing steps that get executed, allowing
technical artists to better optimize content and set up custom, game-specific asset pipelines.

This is handled through [*Creation Graphs*]({{base_url}}creation_graphs/concept.html). A *Creation Graph* is essentially a generic framework for
processing arbitrary data on the CPUs and GPUs, exposed through a graph front-end view. While we can
use *Creation Graphs* for any type of data processing. 

For more information visit the [*Creation Graphs*]({{base_url}}creation_graphs/concept.html) section.

> **Tip:**  if you wish to see other use cases such as particle systems, sky rendering and sprite sheets, then have a look in the
> [`creation_graphs`](https://ourmachinery.com/samples.html) sample that we provide. 

## Importing a DCC asset

You can import an asset by selecting **File > Import...** in the main menu, pressing **Ctrl-I**, or dropping a DCC file on the Asset Browser tab. When you do this, it ends up in our data-model as a `dcc_asset`. 

For a more in detail explanation about how to import assets checkout the [Asset Import Part]({{base_url}}editing_workflows/import_assets.html).

### Basic entity rigging, with image and material extraction

If you click on a `dcc_asset` that contains a mesh in the Asset Browser, you will be presented
with importer settings in the Properties tab:

![Inspecting a `dcc_asset`](https://www.dropbox.com/s/n6njdkl84dzem8n/dcc-asset-before-entity-rig.png?raw=1)

The Preview tab does just enough to show you what the `dcc_asset` contains, but what you probably
want is an `entity` that contains child entities representing the meshes found inside the
`dcc_asset`. Also, you probably want it to extract the images and materials from the `dcc_asset` so
you can continue to tweak those inside The Machinery. There are two ways to do this. Either you drag
the DCC asset onto the *Scene Tab*, or you click the *Import Asset* button. The *Import Assets*
button will automatically create a prototype Entity Asset in your project, while dropping it into
the scene will rig the entity inside the scene, without creating a prototype.

In either case, we will for our `door.dcc_asset` get a `door.resources` directory next to it. This
directory will contain materials and images extracted from the DCC asset. If you prefer dropping
the assets into the scene directly, but also want an entity prototype, then you can check the
`Create Prototype on Drop` check box.

Each image and material in the resources folder is a *Creation Graph*, which is responsible for the
data-processing of those resources. You can inspect these graphs to see what each one does. They are
described in more detail below.

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/loaYaeSl-_g?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=ourmachinery.com"></iframe>

### Creation Graphs for `dcc_asset` import

In The Machinery, there are no specific asset types for images or materials, instead, we only have
*Creation Graphs* (`.creation` assets). To extract data from a `dcc_asset` in a creation graph, the
`dcc_asset`-plugin exposes a set of helper nodes in the *DCC Asset* category:

* `DCC Asset/DCC Image` -- Takes the source `dcc_asset` together with the name of the image as input
  and outputs a `GPU Image` that can be wired into various data processing nodes (such as mipmap
  generation through the `Image/Filter Image` node) or directly to a shader node.

* `DCC Asset/DCC Material` -- Takes the source `dcc_asset` together with the name of the material as
  input and outputs all properties of the material model found inside the `dcc_asset`. This material
  representation is a close match to GLTF 2.0's PBR material model. Image outputs are references to
  other `.creation` assets which in turn output `GPU Images`.

* `DCC Asset/DCC Mesh` -- Takes the source `dcc_asset` together with the name of the mesh as input
  and outputs a `GPU Geometry` that can be wired to an `Output/Draw Call` output node for rendering
  together with the minimum and maximum extents of the geometry that can be wired to an
  `Output/Bounding Volume` output node for culling.

The steps for extracting images and material `.creation` assets from a `dcc_asset` involve deciding
what data-processing should be done to the data before it gets wired to an output node of the graph.
This can either be done by manually assembling creation graphs for each image and material, or by
building a generic creation graph for each asset *type* and use that as a prototype when running a
batch processing step we refer to as *Resource Extraction*.

Here's an example of what a generic creation graph prototype for extracting images might look like:

![Simple image processing.](https://www.dropbox.com/s/z2e3s5w1h8yiv1k/image-cg.png?raw=1)

To quickly get up and running we provide a number of pre-authored creation graphs for some of the
more common operations:

* `import-image`-- Operations applied to images imported directly into the editor (not as part of a
  `dcc-asset`).

* `dcc-image` -- Operations applied to images extracted from an imported `dcc_asset`.

* `dcc-material` -- Shader graph setup to represent materials extracted from an imported `dcc_asset`.

* `dcc-mesh` -- Operations for generating a draw call that represents a mesh from an imported `dcc_asset`.

* `drop-image` -- Operations for generating a draw call to display the image output of another
  creation graph in the context of an entity, making it possible to drag-and-drop images into the
  Scene Tab.

These pre-authored creation graphs are shipped as part of our Core project which is automatically
copied into new projects. How they are used when working with assets is exposed through the
`import_settings` asset:

![Default Import Settings.](https://www.dropbox.com/s/sr52qac8i1i757l/import-settings.png?raw=1)

By exposing these settings through an asset it is possible to easily change the default behavior of
how imported assets are treated when placed under a specific folder. 

> **Note:** It's worth noting that this is somewhat of a power-user feature and not something you need to have a detailed
> understanding of to get started working with The Machinery.
