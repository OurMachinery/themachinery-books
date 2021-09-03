# The Machinery for Unreal 4 Dev's

When migrating from Unreal Engine 4 (UE4) to The Machinery, there are a few things that are different.

**Quick Glossary**

The following table contains common UE4 terms on the left and their The Machinery equivalents (or rough equivalent) on the right.

| UE4                                                          | The Machinery                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Actor, Pawn                                                  | Are composed of Entities and Components and Systems          |
| Blueprint Class (only the inheritance aspect and that they can represent actors) | [Prototypes]({{base_url}}editing_workflows/prototypes.html)  |
| Material Instance, Shaders, Textures, Particle Effects, Static Mesh, Geometry,Skeletal Mesh, Material Editor | [Creation Graphs]({{base_url}}creation_graphs/concept.html)  |
| **UI**                                                       | **UI**                                                       |
| World Outliner                                               | [Entity Tree]({{base_url}}the_editor/entity_tree_tab.html)   |
| Details Panel                                                | [Properties Tab]({{base_url}}the_editor/properties_tab.html) |
| Content Browser                                              | [Asset Browser]({{base_url}}the_editor/asset_browser.html)   |
| Viewport                                                     | [Scene Tab]({{base_url}}the_editor/asset_browser.html)       |
| **Programming**                                              | **Programming**                                              |
| Blueprints                                                   | [Entity Graph]({{base_url}}editing_workflows/visual-scripting.html) |
| C++                                                          | C                                                            |

## Questions you might have

**Where are my Actors?**

The Machinery has no concept of Actors in the sense as UE4 does. The Engine is based around Entities and Components. In the game world, not the editor, everything lives within the Entity Component System (ECS). To be exact, it lives within the Entity Context, an isolated world of entities. Your Actors are split into data and Behaviour. 

You would usually couple your logic together with data in your Actor classes. In The Machinery, you separated them into Components and Systems / Engines. Different behaviour can be achieved via composition rather than via Inheritance.

Components represent data while Systems or Engines represent your behaviour. They operate on multiple entities at the same time. Each Entity Context (the isolated world of Entities) has several systems/engines registered to them.



**Where are my Blueprints?**

The Machinery supports two ways of gameplay coding by default:

1. using our Visual Scripting Language ([Entity Graph]({{base_url}}editing_workflows/visual-scripting.html))
2. using our C API's to create your gameplay code. This way, you can create your Systems/Engines to handle your gameplay.

You do not like C? Do not worry! You can use C++, Zig, Rust, or any other language that binds to C.



**What is the difference between a System and an Engine?**

An Engine update is running on a subset of components that possess some set of components. Some entity component systems are referred to as *systems* instead, but we choose *Engine* because it is less ambiguous.

On the other hand, a system is an update function that runs on the entire entity context. Therefore you can not filter for specific components.

**Where are my Material Instance, Shaders, Textures, Particle Effects, Static Mesh, Geometry, Skeletal Mesh, Material Editor?**

All of these can be represented via the the [Creation Graphs]({{base_url}}creation_graphs/concept.html).



**Project data?**

The Machinery supports two types of Project formats:

1. The Directory Project (Default)

A Source control and human-friendly project format in which your project is stored on Disk in separate files (text and binary for binary data)

1. The Database Project

A single binary file project. It will contain all your assets and data. This format is mainly used at the end to pack your data for the shipping/publishing process.



**Where do I put my assets?**

At this point in time, you can only drag & drop your assets via the Asset Browser as well as via the Import Menu. See more in the section about importing assets. [How to import assets]({{base_url}}editing_workflows/import_assets.html)



**What are common file formats supported?**

| Asset Type | Supported Formats             |
| :--------- | :---------------------------- |
| 3D         | .fbx, .obj, .gltf             |
| Texture    | .png, .jpeg, .bmp ,.tga, .dds |
| Sound      | .wav                          |

Our importer is based on Assimp. Therefore we support most things assimp supports. (We do not support .blend files)



**Where do my source code files go?**

In the Machinery, all we care about is your plugins. Therefore if you want your plugins (tm_ prefixed shared libs.) to be globally accessible, please store them in the /plugins folder of the Engine. An alternative approach is to create plugin_asset in the Engine then your plugin becomes part of your project. 

Please check out the introduction to the [Plugin System]({{base_url}}extending_the_machinery/the_plugin_system.html) as well as the [Guide about Plugin Assets]({{base_url}}extending_the_machinery/plugin-assets.html).



**Using Visual Scripting**

Visual Scripting is a perfect solution for in-game logic flow (simple) and sequencing of actions. It is a great system for artists, designers, and visually oriented programmers. It is important to keep in mind that the Visual Scripting language comes with an overhead that you would not pay in C (or any other Language you may use for your gameplay code).
