# Sample Plugins

The easiest way to build a plugin is to start with an existing example. There are three places where
you can find plugin samples:

1. The `samples` folder in the SDK has a number of plugin samples.

2. The *All Sample Projects* package in the *Download* tab has a `plugins` folder with some small
   samples. You can also find their source code here: [https://github.com/OurMachinery/sample-projects](https://github.com/OurMachinery/sample-projects)
3. You can create a new plugin with the menu command **File > New Plugin**. This will create a
   new `.c` file for the plugin together with some helper files for compiling it. ([Follow this guide]({{base_url}}/extending_the_machinery/write-a-plugin.html#write-your-own-plugin))

The distribution already comes with pre-built .dlls for the sample plugins, such as
`bin/plugins/tm_pong_tab.dll`. You can see this plugin in action by selecting **Tab > Pong** in the
editor to open up its tab:

![Pong tab.](https://www.dropbox.com/s/hats2jgr3wroahz/pong-tab.png?dl=1)

**Table of Content**

* auto-gen TOC;
{:toc}


### What are the build Requirements

To build plugins you need three things:

1. You need to have Visual Studio 2019 installed including the MS C++ Build Tools on your computer.
   Note that the Community Edition works fine. (Or clang and the build essentials on Linux)
2. You need to set the `TM_SDK_DIR` environment variable to the path of the SDK package that you
   installed on your computer. When you compile a plugin, it looks for The Machinery headers in the
   `%TM_SDK_DIR%/headers` folder. 
3. You need the `tmbuild.exe` from the SDK package. `tmbuild.exe` does all the steps needed to
   compile the plugin. Put it in your `PATH` or copy it to your plugin folder so that you can run it
   easily from the command line.

### Build the sample plugin

To compile a plugin, simply open a command prompt in the plugin folder and run the `tmbuild.exe`
executable:

~~~ cmd input
sample-projects/plugins/custom_tab> %TM_SDK_DIR%/bin/tmbuild.exe
​~~~ cmd output
Installing 7za.exe...
Installing premake-5.0.0-alpha14-windows...
Building configurations...
Running action 'vs2019'...
Generated custom_tab.sln...
Generated build/custom_tab/custom_tab.vcxproj...
Done (133ms).
Microsoft (R) Build Engine version 16.4.0+e901037fe for .NET Framework
Copyright (C) Microsoft Corporation. All rights reserved.

  custom_tab.c
  custom_tab.vcxproj -> C:\work\themachinery\build\bin\plugins\tm_custom_tab.dll

-----------------------------
tmbuild completed in: 23.471 s
~~~

`tmbuild.exe` will perform the following steps to build your executable:

1. Create a `libs` folder and download `premake5` into it. (You can set the `TM_LIB_DIR` environment
   variable to use a shared `libs` directory for all your projects.)
2. Run `premake5` to create a Visual Studio project from the `premake5.lua` script.
3. Build the Visual Studio project to build the plugin.

> **Note:** You can learn more about [tmbuild]({{base_url}}helper_tools/tmbuild.html) in its own section.



## Sample Plugins:

| Project                               | Description                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| `samples\plugins\assimp`              | Shows how to write a complex plugin. This is the default assimp importer plugin of the engine. |
| `samples\plugins\atmospheric_sky`     | Shows how to interact with the ECS and the renderer.         |
| `samples\plugins\default_render_pipe` | The source code of our default render pipeline. This can help you in case you want to learn more about the render pipeline |
| `samples\plugins\gltf`                | The source code of our gltf importer                         |
| `samples\plugins\graph_nodes`         | Shows how to implement graph nodes.                          |
| `samples\plugins\pong_tab`            | Shows how to implement a more complex tab.                   |
| `samples\plugins\spin_component`      | Shows how to implement a component and a engine.             |
| `samples\plugins\ui_sample_tab`       | A great playground for our IMGUI UI System.                  |

