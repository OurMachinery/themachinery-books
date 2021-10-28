# Part 2: Running Multiple Network Instances

In this tutorial you’ll learn how to run multiple simulation instances at the same time. This tutorial build on the learnings of the pervious tutorial: [Part 1]({{tutorials}}//network/animation_sample/network_assets.md)

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 

## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/ZKiWW5rvep4?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial
Now that we have setup our two Network Assets we want to make sure that when we start our simulation both a Client and a Server instances are created, each in its own Simulate Tab.

We can do that changing the Network Settings: File→Settings→Networrk Settings: let’s add a Server Instance and a Client Instance.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342679832_image.png)

If we run the simulation now you will see an empty world on the Client: the reason is that the Client Asset has been setup to start with an empty world, and no entities in the Server world are currently being replicated to the Client: Let’s fix this by making the World Entity Replicated via the Entity Tree.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342731213_image.png)

And if we run the simulation again we’ll now see that the Client is correctly receiving updates from the Server about the World Entity: we can move the Xbot Entity in both windows exactly like in the single player game, but now when we move on the Server Window you’ll notice that the updates are sent to the Client as well: that is because we automatically check for changes in the components of all the entitites that have been flagged as replicated (once per second by default).

 If we instead move the Player from the Client window, you’ll see that the Player on the Server entity doesn’t get updated: we told the Client to have a passive Gamestate, and so even if the Client is simulating the Player on its own simulation instance it doesn’t send the updates to the Server.

 

 

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343311632_image.png)