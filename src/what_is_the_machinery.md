# What is The Machinery?

*The Machinery* is a framework for building different kinds of 3D software: editors, tools, pipeline components, games, visualizations, simulations, toys, experiments etc. You can think of it as a *game engine*, but its intended use stretches beyond games, covering a wide range of applications. What makes *The Machinery* special is that it is *lightweight* and completely *plugin-based*. This means that you are not limited to a single editor and runtime. Rather, you can mix and match components as you need (or write your own) to create your own unique experience. *The Machinery* can also be stripped down and run embedded, as part of a larger application.

## A toolbox of building blocks

![](https://ourmachinery.com/images/headers/header_plugins.png)

The Machinery is completely plugin-based. You can pick and choose the parts you need to customize it to your specific needs. You can extend the engine, and the editor, by writing your own plugins. You can even build completely new applications on top of our API, or embed our code into your existing applications or workflows.

- [The Plugin System]({{base_url}}extending_the_machinery/the_plugin_system.html)

## Powerful editing model

![](https://ourmachinery.com/images/headers/header_collaboration.png)

The Machinery uses a powerful data model called *The Truth*. This model is used to represent assets and has built-in support for serialization, streaming, copy/paste, drag-and-drop as well as unlimited undo/redo. It supports an advanced hierarchical prototyping model for making derivative object instances and propagating changes. It even has full support for real-time collaboration, multiple people can work together in the same game project, Google Docs-style. Since all of these features are built into the data model itself, your custom game-specific data will get them automatically, without you having to write a line of code.

- [The Truth]({{base_url}}the_truth/index.html)
- [Collaboration]({{base_url}}the_truth/collaboration.html)

## Easy to build tools

![](https://ourmachinery.com/images/headers/header_tools.png)

The Machinery uses an in-house, lightweight Immediate GUI (IMGUI) implementation, it is used for both the editor UI as well as any runtime UI the end-user needs. Extending the editor UI using custom plugins is simple and the possibility to *Hot Reload* code makes creating new UIs a breeze.

Using our UI APIs, it is easy to create custom UI controls. And everything has been optimized to feel snappy and responsive. In fact, the entire editor UI is rendered with just a single draw call.

- [UI System]({{base_url}}tutorials/ui/index.html)


## Modern rendering architecture

![](https://ourmachinery.com/images/headers/header_creation-graphs_1920x1080.png)

The renderer has been designed to take full advantage of modern low level graphic APIs. We currently provide a Vulkan backend. A Metal 2 backend is in the works. You can reason explicitly about advanced setups such as multiple GPUs and GPU execution queues. Similar to the rest of the engine, the built-in rendering pipeline is easy to tweak and extend -- we ship the source code for the high-level parts of the rendering pipeline with all versions of The Machinery, including the [Indie Free]({{https://ourmachinery.com/pricing.html}}) version.

- [Graphics]({{base_url}}graphics/index.html)
- [Creation Graphs]({{base_url}}creation_graphs/concept.html)


## High performance

![](https://ourmachinery.com/images/headers/header_jobs.png)

The Machinery focuses a lot on making the engine fasts by focusing on data flows and cache friendly memory layouts, we strive towards using data-oriented design principles. Code that needs to be heavily parallelized can run on top of our fiber-based job system, taking full advantage of the parallel processing power of modern CPUs. We also have a thread-based task system for more long-running tasks.

- [Concurrency in Machinery]({{base_url}}getting_started/introduction_to_c/concurrency.html)


## Simplicity

![](https://ourmachinery.com/images/headers/header_hot_reload.png)

The Machinery aims to be simple, minimalistic and easy to understand. In short, we want to be "hackable". All our code is written in plain C, a significantly simpler language than modern C++. The entire code base compiles in less than 60 seconds and we support hot-reloading of DLLs, allowing for fast iteration cycles.

Our APIs are exposed as C interfaces, which means they can easily be used from C, C++, Rust or any other language that has a FFI for calling into C code.

- [Introduction in C programming in the Machinery]({{base_url}}getting_started/introduction_to_c/index.html)
- [Programming Guidebook](https://ourmachinery.com/apidoc/doc/guidebook.md.html)
- [Extending The Machinery]({{base_url}}extending_the_machinery/index.html)
- [Write a Plugin]({{base_url}}extending_the_machinery/write-a-plugin.html)

