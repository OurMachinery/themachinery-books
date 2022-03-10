# Part 3: Entity Control

In this tutorial you’ll learn how to set the control of a specific entity and remap its input source. This tutorial build on the learnings of the pervious tutorial: [Part 2]({{base_url}}/tutorials/network/animation_sample/multiple_network_instances.html)

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 

## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/7nDhbiTRH8c?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial
We now want to make sure that the movement and facing direction of our player on the *Server* are controlled by the Keyboard and mouse input that is detected on the *Client.*

There’s a special purpose node that we can use to do exactly that: let’s add a “Set Entity Control” node to the Entity Graph of the World Entity: we want to bind the control of the *xbot* entity to the Client that connects to our server, so we will take the output from the *Connection Accepted* node and chain it to the *Set Entity Control* node.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342858285_image.png)

We also need to tell the server that it should use the input that comes from the *Client* for the *xbot* Entity: we can use the *Remap Input* node to do so.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342886611_image.png)

We also need to tell the *Client* that the input for the *Xbot* entity has to be taken from its own keyboard/mouse input: we’ll add the *Remap input* node as well once the *Acquired Entity Control* event is triggered on the client.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342925053_image.png)

Now that we’ve remapped the input to come from the correct source, let’s convert all of the *Poll Key* and *Poll Mouse Motion* nodes in *Poll Key for Entity* and *Poll Mouse Motion for Entity* in the Graph of the *xbot* entity: this will make sure that instead of blindly using the local input to drive this entity, we’ll be a bit more smart and use the correct input: either the local one (Client) or the remote one that comes from the Client (Server). You can do this by using the “Covert” feature: right click on a node and click “convert” to see all the nodes that you can convert that node into.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343013043_image.png)

So the Client is now transmitting the Input to the server (while using the keyboard/mouse input to drive it’s own player entity), and the *server* is instead using that input to drive its simulation instead.