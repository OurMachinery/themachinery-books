# Basic editing workflow

The basic scene editing workflow in *The Machinery* looks something like this:

1. Import some asset files into the Asset Browser using **File > Import…** If you don't have any
   models to work with you can find free ones at [Sketchfab](https://sketchfab.com) for example.

2. Organize the files by right-clicking the Asset Browser and choosing **New > New Folder** and by
   dragging and dropping.

3. Any imported model, for example `fbx` or `gltf`, will appear as a `dcc_asset`.

4. Rig an entity from the `dcc_asset` by selecting it and clicking *Import Assets* in the property
   panel. This also imports the materials and images inside the `dcc_asset`.

5. Double click the imported entity to open it for editing.

6. Add components for physics, animation, scripting, etc to the entity.

7. Open a scene entity that you want to place your imported entity inside. A new project has a scene
   entity called `world.entity` that you can use. Or you can create your own scene entity by right
   clicking in the Asset Browser and choosing **New > New Entity**.

8. Drag your asset entities into the scene entity to position them in the scene.

9. Use the Move, Rotate, and Scale tools in the Scene tab to arrange the sub-entities.

10. Holding down *shift* while using the move tools creates object clones.

11. Select entities or components in the Entity Tree and Scene tabs to modify their properties using the
    Properties Tab.

12. Drag and drop in the Entity Tree Tab to re-link entities.

13. Each tool (Move, Rotate and Scale) has tool-specific settings, such as snapping and pivot point, in
    the upper-left corner of the scene tab.

14. Use **Scene > Frame Selection** and **Scene > Frame Scene** to focus the
    camera on a specific selected entity, or the entire scene. Or just use the _F key_.

15. When you are done, use **File > Save Project…** to save the scene for future
    work.

>  **Known issues:** When you drag a tab out of the current window to create a new one, you don’t
> get any visual feedback until the new window is created.
