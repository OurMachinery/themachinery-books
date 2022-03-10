# Part 6: Smooth Animation

In this tutorial you’ll learn how to synchronize an animation across multiple simulation instances. This tutorial build on the learnings of the pervious tutorial: [Part 5]({{base_url}}/tutorials/network/animation_sample/basic_graph_variables.html)

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 


## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/ZLFbNz_uFrw?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial

Even if the orientation of each player is now correctly broadcasted, movement its not: we’d like to make it so each client receives the correct information about where each other client is moving, so that it can play the *animation* correctly.

Take a look at the *WASD subgraph* section of the *xbot* entity: 

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343896237_image.png)

We want to inject some *float variable network replication* nodes on the float (green) connections to make it so that only the client that controls a specific player entity sets and replicates the movement variables: the value will be transmitted to the server, which will in turn broadcast it to all the other clients. (Exactly the same strategy we used for the facing direction). On the other hand, all the simulations running should *Get* the variable value (either from their own computation or from the network) and pass that value to the *Animation Set Variable* nodes. 

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343687819_image.png)

Important note: even if *Set if* is true in the *float variable network replication* node, the variable won’t actually be set if you don’t have control over that particular entity. Otherwise each simulation instance would override the variables of each other client as well as their own.

Now all the player entities move smoothly on all the clients, and we added multiplayer support to the player movement code by just “hijacking” those four connections and injecting some network replication nodes in the middle of them.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635344207286_image.png)