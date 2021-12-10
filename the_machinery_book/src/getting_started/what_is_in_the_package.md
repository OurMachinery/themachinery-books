# What is in this package?

In the distribution package you will find this:

| Folder                               | Content                                                      |
| ------------------------------------ | ------------------------------------------------------------ |
| **headers/**<br>**lib/**<br>**bin/** | The headers, libraries, and DLLs that make up *The Machinery* SDK. |
| **bin/the‑machinery.exe**            | The Machinery's main editor.                                 |
| **doc/**                             | SDK  documentation.                                          |
| **samples/**                         | Sample code that shows how to extend the editor and SDK with plugins, as well as how to build new executables on top of *The Machinery.* |
| **code/**                            | For reference: code for our utility programs.                |
| **bin/simple‑draw.exe**              | A simple drawing program built on top of the SDK.            |
| **bin/simple-3d.exe**                | A simple 3D viewport built on top of the SDK.                |
| **bin/tmbuild.exe**                  | Our build tool, that can be used to build samples and plugins. |
| **bin/docgen.exe**                   | Our tool for generating documentation.                       |
| **bin/hash.exe**                     | Our tool for generating static hash strings.                 |
| **bin/localize.exe**                 | Our tool for generating localization data.                   |
| **bin/runner.exe**                   | An executable that can load a The Machinery project and do what Simulate Tab does, but stand-alone. It is copied whenever you Publish a project from within The Machinery. |
| **utils/.clang-format**              | The clang-format settings we use to format our code.         |
| **utils/pre-commit**                 | The pre-commit hook we use in our git repository to auto-format the code. |
| **utils/enable-full-dumps.reg**      | A registry file that enables full crash dumps (see below).   |

You can use the *Download* tab inside The Machinery to download sample projects for the engine.

Here's a list of the sample projects that are available:

| Project                         | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| **Animation**                   | A sample project that features an animated character.        |
| **Creation Graphs**             | Sample use of creation graphs.                               |
| **Gameplay First Person**       | A sample first-person game.                                  |
| **Gameplay Interaction System** | A sample first-person game with intractable entities.        |
| **Gameplay Third Person**       | A sample third-person game.                                  |
| **Modular Dungeon Kit**         | A sample modular project that lets you compose dungeon scenes out of modular components. |
| **Physics**                     | A sample project that demonstrates the use of physics.       |
| **Pong**                        | A sample visual scripting and gameplay project.              |
| **Ray Tracing: Hello Triangle** | A sample project showing how to use the ray tracing APIs.    |
| **Sound**                       | A sample project demonstrating sound playback.               |
| **All Sample Projects**         | A zip containing all sample projects.                        |


The `All Sample Projects` download contains all these projects, and also some sample engine plugins
that can get you started with extending the engine.

Note that some of the content in these projects was created by other people and licensed under
Creative Common or other licenses. See the `*-license.txt` files in the projects for attribution and
license information.

The editor that is included allows you to:

- Import various types of DCC assets (FBX, GLTF, etc).
- Create simple entities/scenes by placing and arranging assets.
- Add scripted behaviors to entities using the visual scripting language in the *Entity Graphs*.
- Add physics collision to objects and modify their physical properties.
- Import animations and create advanced animation setups as an *Animation State Machine*.
- Import WAV files and play them or place them on entities.
- Run and simulate these behaviors using the *Simulate* tab.
- Extend the engine and the editor with your own plugins that implement new editor tabs, entity components, gameplay code, etc.
- Write your own applications, using *The Machinery* as an SDK.
