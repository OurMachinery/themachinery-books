# The Machinery for Godot Dev's

When migrating from Godot to The Machinery, there are a few things that are different.

**Table of Content**

* auto-gen TOC;
{:toc}


**Quick Glossary**

The following table contains common Godot terms on the left and their The Machinery equivalents (or rough equivalent) on the right.

| Godot                                                        | The Machinery                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Nodes                                                        | Are composed of Entities and Components and Systems          |
| Materials, Shaders, Textures, Particle Effects, Mesh, Geometry, Shader Graph, Material Editor | [Creation Graphs]({{base_url}}creation_graphs/concept.html)  |
| **UI**                                                       | **UI**                                                       |
| Scene                                                        | [Entity Tree]({{base_url}}the_editor/entity_tree_tab.html)   |
| Inspector                                                    | [Properties Tab]({{base_url}}the_editor/properties_tab.html) |
| FileSystem                                                   | [Asset Browser]({{base_url}}the_editor/asset_browser.html)   |
| Viewport                                                     | [Scene Tab]({{base_url}}the_editor/asset_browser.html)       |
| **Programming**                                              | **Programming**                                              |
| VisualScript                                                 | [Entity Graph]({{base_url}}editing_workflows/visual-scripting.html) |
| C#, GDScript, C++                                            | C                                                            |

## Questions you might have

### Where are my Nodes?

The Machinery has no concept of Nodes in the sense as Godot does. The Engine is based around Entities and Components.

Everything within the Game World lives within the Entity Component System (ECS). To be exact, it lives within the Entity Context, an isolated world of entities. Your Nodes are split into data and behaviour.

You would usually couple your logic together with data when working in Godot. This coupling happens because Godot uses the Object-oriented approach while The Machinery uses the Data-Oriented approach. Hence you would inherit classes to compose different kinds of behaviour. 



In The Machinery, you separated them into Components and Systems / Engines. They represent your data and Systems or Engines that represent your Behaviour. They operate on multiple entities at the same time. Each Entity Context (the isolated world of Entities) has several systems/engines registered to them. In the following image we broke down an example player in Godot into separate parts (components) and its methods into separate Engines.

![](https://www.dropbox.com/s/mw0hb5itj5zck7g/tm_guide_object_to_ecs.png?dl=1)

Important to understand is that the Player Class on the left does not equal the Entity on the left! Since the Entity on the left is just a weak reference to the components, it does not own the data, unlike the Player Class. The Components together form the player and the Systems/Engines on the far right just consume a few of those components, they do not need to understand them all!

This setup allows you to compose entities that are reusing the same engines/systems! For example all your other entities that can move can use the Movement Engine and Jump Engine to get the jump function.  All you need to do is compose entities with the:

- Transform Component
- Physics Mover Component
- Jump Component
- Movement Component

The Movement Engine and Jump Engine will pick them up and apply the same logic to them!



#### What is the difference between a System and an Engine?

An Engine update is running on a subset of components that possess some set of components. Some entity component systems are referred to as *systems* instead, but we choose *Engine* because it is less ambiguous.

On the other hand, a system is an update function that runs on the entire entity context. Therefore you can not filter for specific components. For more information see [the chapter about the Entity Component System]({{the_machinery_book}}/gameplay_coding/ecs/index.html).



### How do I script?

The Machinery supports two ways of gameplay coding by default:

1. using our Visual Scripting Language ([Entity Graph](https://ourmachinery.github.io/themachinery-books/the_machinery_book/editing_workflows/visual-scripting.html))
2. using our C APIs to create your gameplay code. This way, you can create your Systems/Engines to handle your gameplay.

You do not like C? Do not worry! You can use C++, Zig, Rust, or any other language that binds to C.

### Where are my Materials, Shaders, Textures, Particle Effects?

All of these can be represented via the [Creation Graphs](https://ourmachinery.github.io/themachinery-books/the_machinery_book/creation_graphs/concept.html).

### Project data?

The Machinery supports two types of Project formats:

1. The Directory Project (Default)

Source control and human-friendly project format in which your project is stored on Disk in separate files (text and binary for binary data)

1. The Database Project

A single binary file project. It will contain all your assets and data. This format is mainly used at the end to pack your data for the shipping/publishing process.



### Where do I put my assets?

At this point in time, you can only drag & drop your assets via the Asset Browser as well as via the Import Menu. See more in the section about importing assets. [How to import assets](https://ourmachinery.github.io/themachinery-books/the_machinery_book/editing_workflows/import_assets.html)



### What are common file formats supported?

| Asset Type | Supported Formats             |
| :--------- | :---------------------------- |
| 3D         | .fbx, .obj, .gltf             |
| Texture    | .png, .jpeg, .bmp ,.tga, .dds |
| Sound      | .wav                          |

Our importer is based on Assimp. Therefore we support most things assimp supports. (We do not support .blend files)



### Where do my source code files go?

In the Machinery, all we care about is your plugins. Therefore if you want your plugins (tm_ prefixed shared libs.) to be globally accessible, please store them in the /plugins folder of the Engine. An alternative approach is to create plugin_asset in the Engine then your plugin becomes part of your project.

Please check out the introduction to the [Plugin System](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/the_plugin_system.html) as well as the [Guide about Plugin Assets](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/plugin-assets.html).



### Using Visual Scripting

Visual Scripting is a perfect solution for in-game logic flow (simple) and sequencing of actions. It is a great system for artists, designers, and visually oriented programmers. It is important to keep in mind that the Visual Scripting language comes with an overhead that you would not pay in C (or any other Language you may use for your gameplay code).



