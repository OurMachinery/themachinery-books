# Creation Graphs for Unity Developers

Creation graphs are used for many different assets in The Machinery. When a creation graph is used for a surface shader it most closely relates to Unity’s shader graph. This is what we will focus on first.

![Simple surface shader](https://paper-attachments.dropbox.com/s_04714ABB7614AA7E464946A69D4D155B5E36439454460DD779DF6945F603E630_1626601618396_image.png)


In the example above the editor’s layout was made to resemble Unity’s shader graph view. When creating a material shader you need to specify a `Shader Instance` output node. From here we can specify out surface shader, in the example above the `Lit` node closely resembles Unity’s `PBR Master` node.