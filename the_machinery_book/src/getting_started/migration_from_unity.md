# The Machinery for Unity Dev's

When migrating from Unity to The Machinery, there are a few things that are different.

**Table of Content**

* auto-gen TOC;
{:toc}


**Quick Glossary**

The following table contains common Unity terms on the left and their The Machinery equivalents (or rough equivalent) on the right.

| Unity                                                        | The Machinery                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| GameObjects                                                  | Are composed of Entities and Components and Systems          |
| Prefabs                                                      | [Prototypes]({{base_url}}editing_workflows/prototypes.html)  |
| Materials, Shaders, Textures, Particle Effects, Mesh, Geometry, Shader Graph, Material Editor | [Creation Graphs]({{base_url}}creation_graphs/concept.html)  |
| **UI**                                                       | **UI**                                                       |
| Hierarchy Panel                                              | [Entity Tree]({{base_url}}the_editor/entity_tree_tab.html)   |
| Inspector                                                    | [Properties Tab]({{base_url}}the_editor/properties_tab.html) |
| Project Browser                                              | [Asset Browser]({{base_url}}the_editor/asset_browser.html)   |
| Scene View                                                   | [Scene Tab]({{base_url}}the_editor/asset_browser.html)       |
| **Programming**                                              | **Programming**                                              |
| Bolt                                                         | [Entity Graph]({{base_url}}editing_workflows/visual-scripting.html) |
| C#                                                           | C                                                            |

## UI Differences

**Unity**

![](https://www.dropbox.com/s/0a47vz1walkm79r/tm_guide_unity_editor.png?dl=1)

**The Machinery**

![](https://www.dropbox.com/s/67sdkq7sxnkbkou/tm_editor.png?dl=1)

1. The **Main Menu**: It allows you to navigate through the Engine, such as opening new tabs or import assets
2. The **Entity Tree** shows a tree view of the entity you are editing. It shows the entity's components and child entities. You start editing an entity by double-clicking it in the asset browser. 
3. The **Scene** shows an editable graphic view of the edited entity. You can manipulate components and child entities by selecting them. Use the *Move*, *Rotate*, and *Scale* gizmos for your desired action.
4. The **Simulate current scene** button will open the **Simulate** tab that lets you "run" or "simulate" a scene.
5. The **Properties** tab shows the properties of the currently selected object in the Scene. You can modify the properties by editing them in the properties window.
6. The **Console** tab shows diagnostic messages from the application.
7. The **Asset Browser** shows all the assets in the project and enables you to manage them.
8. The **Preview** shows a preview of the currently selected asset in the asset browser.

The Editor is a collection of editing *Tabs*, each with its specific purpose. You can drag tabs around to rearrange them. When you drag them out of the window, a new window opens. Use the *View* menu to open new tabs.



## Questions you might have

### Where are my GameObjects?

The Machinery has no concept of GameObjects in the sense as Unity does. The Engine is based around Entities and Components. In the game world, not the editor, everything lives within the Entity Component System (ECS). To be exact, it lives within the Entity Context, an isolated world of entities. Your GameObjects are split into data and Behaviour. 

You would usually couple your logic together with data in your C# MonoBehaviour scripts. In The Machinery, you separated them into Components and Systems / Engines. They represent your data and Systems or Engines that represent your Behaviour. They operate on multiple entities at the same time. Each Entity Context (the isolated world of Entities) has several systems/engines registered to them.

#### What is the difference between a System and an Engine?

An Engine update is running on a subset of components that possess some set of components. Some entity component systems are referred to as *systems* instead, but we choose *Engine* because it is less ambiguous.

On the other hand, a system is an update function that runs on the entire entity context. Therefore you can not filter for specific components.



### Where are my Prefabs?

What Unity calls Prefabs is more or less what we call [Prototypes]({{base_url}}editing_workflows/prototypes.html). Our prototype system allows entity assets to be used inside other entities. Therefore, you can create an entity asset that represents a room and then creates a house entity that has a bunch of these room entities placed into it. For more information on Prototypes, check out its [Prototypes]({{base_url}}editing_workflows/prototypes.html).



### How do I script?

The Machinery supports two ways of gameplay coding by default:

1. using our Visual Scripting Language ([Entity Graph]({{base_url}}editing_workflows/visual-scripting.html))
2. using our C API's to create your gameplay code. This way, you can create your Systems/Engines to handle your gameplay.

You do not like C? Do not worry! You can use C++, Zig, Rust, or any other language that binds to C.



### Where are my Materials, Shaders, Textures, Particle Effects?

All of these can be represented via the [Creation Graphs]({{base_url}}creation_graphs/concept.html).

### Project data?

The Machinery supports two types of Project formats:

1. The Directory Project (Default)

A Source control and human-friendly project format in which your project is stored on Disk in separate files (text and binary for binary data)

1. The Database Project

A single binary file project. It will contain all your assets and data. This format is mainly used at the end to pack your data for the shipping/publishing process.

### Where do I put my assets?

At this point in time, you can only drag & drop your assets via the Asset Browser as well as via the Import Menu. See more in the section about importing assets. [How to import assets]({{base_url}}editing_workflows/import_assets.html)

### Import difference between Unity and The Machinery: `.dcc_asset`

When importing assets created in e.g. Maya they will be imported as `dcc_asset`. A `dcc_asset` can hold all types of data that was used to build the asset in the DCC-tool, such as objects, images, materials, geometry and animation data.

During the import step, The Machinery only runs a bare minimum of data processing, just enough so that we can display a visual representation of the asset in the *Preview* tab. Imports run in the background so you can continue to work uninterrupted. When the import finishes the asset will show up in the *Asset Browser*. 

> **Note** that import of large assets can take a significant amount of time. You can monitor the progress of the import operation in the status bar.

For more information see  [How to import assets]({{base_url}}editing_workflows/import_assets.html) or checkout our [Example Workflow for Importing an Asset and create an Entity]({{the_machinery_book}}/editing_workflows/asset_pipeline.html)

### What are common file formats supported?

| Asset Type | Supported Formats             |
| :--------- | :---------------------------- |
| 3D         | .fbx, .obj, .gltf             |
| Texture    | .png, .jpeg, .bmp ,.tga, .dds |
| Sound      | .wav                          |

Our importer is based on Assimp. Therefore we support most things assimp supports. (**We do not support .blend files**)

*See the [Import Chapter for more details]({{the_machinery_book}}/editing_workflows/import_assets.html)*



### Where do my source code files go?

In the Machinery, all we care about is your plugins. Therefore if you want your plugins (tm_ prefixed shared libs.) to be globally accessible, please store them in the `/plugins` folder of the Engine. An alternative approach is to create plugin_asset in the Engine then your plugin becomes part of your project. 

Please check out the introduction to the [Plugin System]({{base_url}}extending_the_machinery/the_plugin_system.html) as well as the  [Guide about Plugin Assets]({{base_url}}extending_the_machinery/plugin-assets.html).



### Using Visual Scripting

Visual Scripting is a perfect solution for in-game logic flow (simple) and sequencing of actions. It is a great system for artists, designers, and visually oriented programmers. It is important to keep in mind that the Visual Scripting language comes with an overhead that you would not pay in C (or any other Language you may use for your gameplay code).



