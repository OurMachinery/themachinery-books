# Import assets

This walkthrough shows how to import assets into a project and how to use them.

This part will cover the following topics:

- How to import Assets into the Editor
- How to import Assets into the Editor via url
- Import Asset pipeline

**Table of Content**

* {:toc}
## Import differences between Meshes and Textures

Assets that are created by e.g. Maya will be of type after they are imported.  Where DCC stands for Digital Content Creation.  Materials wont be imported untill the `dcc_asset` has been dragged into the scene or used otherweise.

A `dcc_asset` can hold all types of data that was used to build the asset in the DCC-tool, such as objects, images, materials, geometry and animation data.

During the import step, The Machinery only runs a bare minimum of data processing, just enough so that we can display a visual representation of the asset in the *Preview* tab. Imports run in the background so you can continue to work uninterrupted. When the import finishes the asset will show up in the *Asset Browser*. 

> **Note** that import of large assets can take a significant amount of time. You can monitor the progress of the import operation in the status bar.

Textures on the the otherhand will be imported as *creation graphs*. 

## Major supported formats

At the time of writing this walkthrough, The Machinery is supporting the following formats:

> **Note**: Not all formats have been tested that extensivly.

| Format                         | File Ending        |
| ------------------------------ | ------------------ |
| fbx                            | .fbx               |
| GLTF Binary                    | .glb               |
| GLTF                           | .gltf              |
| wav                            | .WAV               |
| dae                            | .dae               |
| obj                            | .obj               |
| stl                            | .stl               |
| jpeg                           | .jpeg              |
| pg                             | .pg                |
| png                            | .png               |
| tga                            | .tga               |
| bmp                            | .bmp               |
| Windows Shared lib dll         | .dll               |
| Linux shared lib so            | .so                |
| The Machinery Theme            | .tm_theme          |
| The Machinery Spritesheet      | .tm_spritesheet    |
| The Machinery database project | .the_machinery_db  |
| The Machinery Directoy Project | .the_machinery_dir |
| zip                            | .zip               |
| 7z                             | .7z                |
| tar                            | .tar               |

> A complete list can be found on the bottom of this page



## How to import assets into the project

The Machinery has three different ways of importing assets. The Import local files, Import remote files, Drag and Drop.

### Import via the file menu

The first method of important an asset is via the **File** menu. There, we have an entry called *Import File,* which opens a file dialog. There you can import any of the supported file formats. *Import File* allows for importing any supported asset archive of the type zip or 7zip. This archive will be unpacked and recursively checked for supported assets.
![](https://www.dropbox.com/s/kb50fpjuqwz7o6o/tm_guide_import_assets.png?raw=1)

### Import from URL


It is possible to import assets from a remote location. In the **File** menu, the entry *Import from URL* allows for importing any supported asset archive of the type zip or 7zip. This archive will be unpacked and recursively checked for supported assets.

![](https://paper-attachments.dropbox.com/s_8A68AE93396574AC0D937BFA8CFC626D302DBC4E0617A82A7B5162043ADD88EF_1615467083098_image.png)

> **Note:** The url import does not support implicitly provided archives or files such as https://myassetrepo.tld/assets/0fb778f1ef46ae4fab0c26a70df71b04 only clear file paths are supported.  For example: https://myassetrepo.tld/assets/tower.zip



### Drag and drop

The next method is to drag and drop either a zip/7zip archive into the asset browser or an asset of the supported type.





## Adding the asset to our scene

In The Machinery a scene is composed of entities. The engine does not have a concept of scenes like other engines do. A dcc_asset that is dragged into the scene automatically extracts its materials and textures etc. into the surrounding folder and adds an entity with the correct mash etc. to the Entity view.

![](https://paper-attachments.dropbox.com/s_8A68AE93396574AC0D937BFA8CFC626D302DBC4E0617A82A7B5162043ADD88EF_1615468046484_drag_dcc_asset.gif)


Another way of extracting the important information of a DCC asset is it to click on the DCC asset in the asset browser and click the button "Extract Assets" in the properties panel. 
This will exactly work like the previous method, but the main difference is that it creates a new entity asset that is not added to the scene. 

Entity assets define a prototype in The Machinery. They are distinguished in the Entity Tree with yellow instead of white text. This concept allows having multiple versions of the same entity in the scene but they all change if the Prototype changes.


## About Import Setting

You can define the import creation graph prototype there as well.

- For Images
- For Materials
- For Meshes

Every DCC asset allows changing of the extraction configuration. Therefore it is possible to define the extraction locations for outputs, images and materials.

Instead of importing assets and change their the configuration per asset , it is possible to define them per folder. All you need to do is add an "*Import Settings Asset*" in the correct folder. This can be done via the asset browser. **Right Click -> New -> Import Settings**

![](https://paper-attachments.dropbox.com/s_8A68AE93396574AC0D937BFA8CFC626D302DBC4E0617A82A7B5162043ADD88EF_1615469368165_image.png)

> **Note:** worth noting that this is somewhat of a power-user feature and not something you need to have a detailed
> understanding of to get started working with The Machinery.

## Video about importing and creating an Entity

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/loaYaeSl-_g?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=ourmachinery.com"></iframe>

## Complete list of supported file formats

At the time of writing this walkthrough, The Machinery is supporting the following formats:

> **Note**: Not all formats have been tested that extensivly.

|format|file ending|
|---------------|---------------|
|3d|.3d|
|3ds|.3ds|
|3mf|.3mf|
|ac|.ac|
|ac3d|.ac3d|
|acc|.acc|
|amf|.amf|
|ase|.ase|
|ask|.ask|
|assbin|.assbin|
|b3d|.b3d|
|bvh|.bvh|
|cob|.cob|
|csm|.csm|
|dae|.dae|
|dxf|.dxf|
|enff|.enff|
|fbx|.fbx|
|glb|.glb|
|gltf|.gltf|
|hmp|.hmp|
|ifc|.ifc|
|ifczip|.ifczip|
|irr|.irr|
|irrmesh|.irrmesh|
|lwo|.lwo|
|lws|.lws|
|lxo|.lxo|
|m3d|.m3d|
|md2|.md2|
|md3|.md3|
|md5anim|.md5anim|
|md5camera|.md5camera|
|md5mesh|.md5mesh|
|mdc|.mdc|
|mdl|.mdl|
|mesh|.mesh|
|mesh.xml|.mesh.xml|
|mot|.mot|
|ms3d|.ms3d|
|ndo|.ndo|
|nff|.nff|
|obj|.obj|
|off|.off|
|ogex|.ogex|
|pk3|.pk3|
|ply|.ply|
|pmx|.pmx|
|prj|.prj|
|q3o|.q3o|
|q3s|.q3s|
|raw|.raw|
|scn|.scn|
|sib|.sib|
|smd|.smd|
|stl|.stl|
|stp|.stp|
|ter|.ter|
|uc|.uc|
|vta|.vta|
|x|.x|
|x3d|.x3d|
|x3db|.x3db|
|xgl|.xgl|
|xml|.xml|
|zae|.zae|
|wav|.WAV|
|ddsexrjpg|.ddsexrjpg|
|jpeg|.jpeg|
|pg|.pg|
|png|.png|
|tga|.tga|
|bmp|.bmp|
|psd|.psd|
|gif|.gif|
|hdr|.hdr|
|pic|.pic|
|Windows Shared lib dll|.dll|
|Linux shared lib so|.so|
|The Machinery Theme|.tm_theme|
|The Machinery Spritesheet|.tm_spritesheet|
|The Machinery database project|.the_machinery_db|
|The Machinery Directoy Project|.the_machinery_dir|
|zip|.zip|
|7z|.7z|
|tar|.tar|