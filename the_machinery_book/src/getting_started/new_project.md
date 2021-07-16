# Getting Started with a New Project

This walkthrough shows how to create a new project. It will also show you what comes by default with the Engine.

This part will cover the following topics:

- Project Pipeline
  - What is the difference between a directory project and a database project?
  - What is a Scene in The Machinery?
  - What comes by default with a project?


Related videos to these topics are:

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/oQGghpCqBhI?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

**Table of Content**

* auto-gen TOC;
{:toc}


# About Projects

Let us talk about the concept behind projects first. In The Machinery, we have two kinds of projects: A database project and a directory project. The difference between both is that a database project results in one file rather than multiple files. It has the file ending .the_machinery_db. This database will contain all your assets. In contrast, a directory project saves all your assets, etc., in a specified project folder. It is possible to save a database project as a directory project and vise versa. 

> Note: If resaving a Database project as a Directory project or vice versa, be aware that these are two different projects. Hence changes to one will not apply to the other.

You handle the main project management steps through the **File Menu.** Such as Create and Save. By default, The Machinery will save your project as a directory project.


# About Scenes

In The Machinery, we do not have a concept of scenes in the traditional sense. All we have are Entities. Therefore any Entity can function as a scene. All you need is to add child entities to a parent Entity. The Editor will remember the last opened Entity. 
When publishing a Game, the Engine will ask you to select your "world" entity. You can decide to choose any of your entities as "world" Entity.

> For more information on publishing, check [here]({{base_url}}/the_machinery_book/editing_workflows/publish.html).

# New Project

After the Machinery has been launched for the first time and the login was successful, the Engine will automatically show you a new empty project. If you do not have an account, you can create an account for free [here](https://ourmachinery.com/sign-up.html), or if you had any trouble, don't hesitate to get in touch with us [here](mailto:ping@ourmachinery.com). 

At any other point in time, you can create a new project via **Files → New Project.**

A new project is not empty. It comes with the so-called "**Core**," a collection of valuable assets. They allow you to start your project quickly. Besides the *Core*, the project will also contain a default World Entity, functioning as your current scene. By default, the world entity includes 2 child entities: *light and post_process*. Those child entities are instances of prototypes. 

> A prototype in The Machinery is an entity that has been saved as an Asset. Prototypes are indicated by yellow text in the Entity Tree View. 
>
> For more information about Prototypes, click [here]({{base_url}}/the_machinery_book/editing_workflows/prototypes.html).


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

You can find more information about gameplay coding in the ["Gameplay Coding" Section]({{base_url}}/the_machinery_book/gameplay_coding/index.html)

