# Getting Started with a New Project

This walkthrough shows how to create a new project. It will also show you what comes by default with the Engine.

This part will cover the following topics:

- Project Pipeline
  - What is the difference between a directory project and a database project?
  - What is a Scene in The Machinery?
  - What comes by default with a project?


**Table of Content**

* {:toc}

# About Scenes

In The Machinery, we do not have a concept of scenes in the traditional sense. All we have are Entities. Therefore any Entity can function as a scene. All you need is to add child entities to a parent Entity. The Editor will remember the last opened Entity. 
When publishing a Game, the Engine will ask you to select your "world" entity. You can decide to choose any of your entities as "world" Entity.

> For more information on publishing, check [here]({{base_url}}editing_workflows/publish.html).

# New Project

After the Machinery has been launched for the first time and the login was successful, the Engine will automatically show you a new empty project. If you do not have an account, you can create an account for free [here](https://ourmachinery.com/sign-up.html), or if you had any trouble, don't hesitate to get in touch with us [here](mailto:ping@ourmachinery.com). 

At any other point in time, you can create a new project via **Files → New Project.**

A new project is not empty. It comes with the so-called "**Core**," a collection of valuable assets. They allow you to start your project quickly. Besides the *Core*, the project will also contain a default World Entity, functioning as your current scene. By default, the world entity includes 2 child entities: *light and post_process*. Those child entities are instances of prototypes. 

> A prototype in The Machinery is an entity that has been saved as an Asset. Prototypes are indicated by yellow text in the Entity Tree View. 
>
> For more information about Prototypes, click [here]({{base_url}}editing_workflows/prototype_workflow/index.html).


![the content of the world entity](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615455893513_image.png)


### The Core
Let us discuss the Core a bit. As mentioned before, the Core contains a couple of useful utilities. They are illustrating the core concepts of the Engine, and they are a great starting point. They can be found in the Asset browser under the core folder:

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615456601483_image.png)


A content overview of the core folder and its subfolders may looks like this:

- A light entity

- A camera entity

- A post-processing stack entity (named post-process in the world entity)

- A default light environment entity

- A post-processing volume entity

- A default world entity (the blueprint of the world entity)

- A bunch of helpful geometry entities. They are in the geometry folder.

  - A sphere entity
  - A box entity
  - A plane entity
  - as well as their geometry material

- A bunch of default creation graphs is in the folder creation_graphs

  - import-image
  - DCC-mesh
  - editor-icon
  - drop-image
  - DCC-material
  - DCC-image

  

## How to add some life to your project

All gameplay can be written in C or a C in any binding language such as C++ or Zig. You can also create gameplay code via the Entity Graph. The Entity Graph would live inside of a Graph Component. You can add that to an Entity. 

You can find more information about gameplay coding in the ["Gameplay Coding" Section]({{base_url}}gameplay_coding/index.html)



## Project Structure Recommendation

It is recommended to separate your gameplay source code, plugin code from the actual project and store them in a separate folder.

```
my_project/game_project // the directory project
my_project/game_plugins // the main folder for all your gameplay code, plugins
```



