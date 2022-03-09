# Part 7: Spawning Entities

In this tutorial you’ll learn how to Spawn an Entity with Prediction.  This tutorial build on the learnings of the pervious tutorial: [Part 6]({{tutorials}}//network/animation_sample/smooth_animation.html)

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 

## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/hBIOyB7yjVY?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial

Let’s see how we can trigger the spawning of an entity on the *server* by pressing a button on the *client.*

First of all let’s make sure that the single player version of the spawning works: setup a single spawn entity node that is triggered when the P button is pressed.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635344803694_image.png)

Then go back to single player mode by just removing all the instances in the network settings and starting the simulation again, verifying that the entity is correctly spawned as the button is pressed.

Now try to run a *client* and a *server* instance at the same time and try to press the button when the focus is on both window:

-if you press the button while the client has focus, nothing will happen as the client has a *passive* gamestate and so even if the event is triggered the client won’t actually spawn any entity.

-if the button is pressed while the server window is in focus, the entity will actually be spawned in the server simulation, and from then on its changes will be propagated to the other connected nodes.

To fix this, let’s convert the *Poll key* node in a *Poll key for Entity* node:

-If we now try to press the button while the focus is on the server nothing will happen, as the server is ignoring the local input for the player

-pressing the button on the client will instead trigger the spawning event on the server (as the input is being replicated)

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635344875508_image.png)

With the current setup, the client has to *wait* for its command to get to the server, be executed, and the entity state changes to come back before it can actually *see* the entity: if you were using this mechanism to spawn a projectile this would mean waiting potentially half a second or more before the player gets some feedback… definitively unacceptable.

Let’s use the *spawn entity with prediction* to let the client create a local copy of the entity that has to be spawned, so that while the packets travel the internet, the client has already “predicted” the new entity creation locally.

But before we can use that node we have to make sure that the *spawning* is done as a consequence of an event (as the event information is what’s used to do the “matching” between the local fake entity and the entity that will later come from the server).

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635344945502_image.png)

Also, we’ll trigger the event only on the *client* and replicate the event itself via the *trigger event network replication* node:

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635345021091_image.png)

We can now finally just convert our *spawn entity* node into a *spawn entity with prediction* node, and the client will correctly spawn (and later match) a fake entity on it’s own local simulation to give an immediate feedback to the player about what happened.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635345050874_image.png)