# Import Projects

The Machinery allows to share and remix the content of projects made within the Engine via the import project feature.

*Project Import* provides an easy way to import assets from one The Machinery project to another. To use it, select **File > Import File…** and pick a The Machinery project file to import. The project you select is opened in a new *Import Project* tab and from there, you can simply drag-and-drop or copy/paste assets into your main project’s *Asset Browser*.

![Importing assets from another project.](https://ourmachinery.com/images/beta_20_11__import_project.png)

*Importing assets from another project.*

When you drag-and-drop or copy-paste some assets, all their dependencies are automatically dragged along so that they are ready to use.

Here is a video showing this in action. We start with a blank project, then we drag in a level from the physics sample and a character from the animation sample, put them both in the same scene, and play:
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/gJpieDfxXQ0?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=ourmachinery.com"></iframe>

To make it even easier to share your stuff, we’ve also added **File > Import from URL…** This lets you import any file that The Machinery understands: GLTF, FBX, JPEG, or a complete The Machinery project directly from an URL. You can even import zipped resource directories in the same way.

For example, in the image below, we imported a Curiosity selfie from NASA (using the URL [https://www.nasa.gov/sites/default/files/thumbnails/image/curiosity_selfie.jpg](https://www.nasa.gov/sites/default/files/thumbnails/image/curiosity_selfie.jpg) ) and dropped it into the scene we just created:

![JPEG imported from URL.](https://ourmachinery.com/images/beta_20_11__import_jpeg.png)

*JPEG imported from URL.*

Have you made something interesting in *The Machinery* that you want to share with the world? Save your project as an *Asset Database* and upload it to a web server somewhere. 

Other people can use the *Import from URL…* option to bring your assets into their own projects.

> **Note**: Be aware when you download plugins from the internet, they might contain plugin assets. Only Trust them if you can trust the source! More on this [See Plugin Assets]({{base_url}}/the_machinery_book/extending_the_machinery/plugin-assets.html)

