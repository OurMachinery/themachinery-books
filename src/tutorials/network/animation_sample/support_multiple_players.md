# Part 4: Supporting Multiple players

In this tutorial you’ll learn how spawn an entity every time a client connects. This tutorial build on the learnings of the pervious tutorial: [Part 3]({{base_url}}/tutorials/network/animation_sample/entity_control.html)

> **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 

## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/n7mkKvf7Z_8?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial

Let’s add support for multiple *Clients* to join the same world.

Instead of referencing a static Entity in the scene, we now want to *spawn* a *new* xbot entity every time a client connects to the server: we can do that simply by converting the *Scene Entity* node into a *Spawn Entity* node.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343132292_image.png)

The other problem we need to solve to effectively support multiple players is the fact that earlier the Camera entity was itself available in the scene: know the camera entity is part of the dynamic entity that we’ll spawn once a client connects, and so the *Set Camera* node has to be executed inside the graph of the *xbot* entity asset itself, once the *Acquired Entity Control* event is triggered.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343166633_image.png)

And now our server fully supports multiple players to join: every time a Client connects to it, it will spawn a new *xbot* entity, set the control and remap the input of it: once the client is notified that it acquired the control of that entity, it will set the camera and remap the input as well.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343426333_image.png)