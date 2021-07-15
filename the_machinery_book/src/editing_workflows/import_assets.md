# Import assets

This walkthrough shows how to import assets into a project and how to use them.

This part will cover the following topics:

- Import Asset pipeline

**Table of Content**

* auto-gen TOC;
{:toc}

Related videos to these topics are:

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/loaYaeSl-_g?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=ourmachinery.com"></iframe>

## How to import assets into the project

The Machinery has three different ways of importing assets. The first method of important an asset is via the **File** menu. There, we have an entry called *Import,* which will open a file dialog. Here one can import any of the supported file formats. At the time of writing this walkthrough, The Machinery is supporting the following formats:

Besides, it is possible to import assets from a remote location. In the **File** menu, the entry *Import from URL* allows for importing any supported asset archive of the type zip or 7zip. This archive will be unpacked and recursively checked for supported assets.

![](https://paper-attachments.dropbox.com/s_8A68AE93396574AC0D937BFA8CFC626D302DBC4E0617A82A7B5162043ADD88EF_1615467083098_image.png)

> Note: The url import does not support implicitly provided archives or files such as https://myassetrepo.tld/assets/0fb778f1ef46ae4fab0c26a70df71b04 only clear file paths are supported.  For example: https://myassetrepo.tld/assets/tower.zip

The next method is to drag and drop either a zip/7zip archive into the asset browser or an asset of the supported type.
Assets that are created by e.g. Maya will be of type “dcc_asset” after they are imported.  Where DCC stands for Digital Content Creation.  While textures will be imported as creation graphs.


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
