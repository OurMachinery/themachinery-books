# Project Setup

Let us talk about the concept behind projects first. In The Machinery, we have two kinds of projects: A database project and a directory project.  It is possible to save a database project as a directory project and vice versa. 

> **Note:** If resaving a Database project as a Directory project or vice versa, be aware that these are two different projects. Hence changes to one will not apply to the other.

## The Directory Project

A directory project saves all your assets, etc., in a specified project folder. This file format is better suited for source control.

![view of a directory project in the Windows explorer](https://www.dropbox.com/s/7xqwlu6yi6y35nz/tm_guide_directory_project.png?dl=1)

## The Asset database Project

The difference between both is that a database project results in one file rather than multiple files. It has the file ending `.the_machinery_db`. This database will contain all your assets.

![database project in the file explorer](https://www.dropbox.com/s/kjmrx89my0olh6z/tm_guide_db_project.png?dl=1)

## Project Management

**Can I directly add Assets to my project from the File Explorer of my OS?**

**No**, the editor will not import assets directly added to the project folder via your OS File Explorer. However you can modify The Machinery files (in a directory project) during runtime or before. If you do this the Engine will warn you.

> Changes to the project on disk where detected: [Import] [Ignore]

More information on this topic [here](https://github.com/OurMachinery/themachinery-public/issues/435).

You handle the main project management steps through the **File Menu.** Such as Create and Save. By default, (1) The Machinery will save your project as a directory project. However you can save your current project as an Asset Database (2).

![](https://www.dropbox.com/s/qosmerpjea1agss/tm_guide_saving_project.png?dl=1)

## Possible folder structure for a project

The following project shows a possible folder structure of a game project. **This is not a recommendation just a suggestion**. At the end it depends on your needs and your workflows how your projects should be structured.

![](https://www.dropbox.com/s/sbdsy1k5wjay89c/tm_guide_possible_folder_structure.png?dl=1)

1. `game_project` contains a The Machinery Directory Project
2. `plugins` contains the dll of  your plugins (should not be checked in into source control)
3. `raw_assets` may contain the raw assets your DCC tool needs to process. Your the Machinery project can point here and you maybe able to just reimport things from there if needed
4. `src` contains the source code of your plugins. They can be in multiple sub folder depending on your liking and need.

**Example `src` folder**

![](https://www.dropbox.com/s/l1429g7p5xx8kj2/tm_guide_possible_subfolder.png?dl=1)

In here we have one single `premake` file and a single `libs.json` as well as the `libs` folder. This allows you to run `tmbuild` just in this folder and all plugins or the ones you want to build can be built at once. Besides it will generate one solution for Visual Studio. In this example all plugins will copy their `.dll/so` files into the `../plugins` folder. 



A possible `.gitignore`

```
plugins/*
src/libs/*
```

as well as the default Visual Studio, Visual Studio Code and C/C++ gitignore content.



