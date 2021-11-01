# Part 5: Basic Graph Variable replication

In this tutorial you’ll learn how to replicate a graph variable across the network.  This tutorial build on the learnings of the pervious tutorial: [Part 4]({{tutorials}}//network/animation_sample/support_multiple_players.html)

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 


## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/b4N9oweGH5E?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial

Even if we’re supporting multiple players, when they move and look around the animation it’s not smooth everywhere: if there are clients A and B connected, nobody is telling client B about where client A is moving or looking, and so client B will only rely on the state updates that comes every second from the server to update the position and orientation of client A in its own simulation.

Let’s first tackle the problem of broadcasting the facing direction of a client to all the other clients.

If you take a look at the *Pan* subgraph of the *xbot* entity, you’ll see that we are computing a small angle offset every frame and adding that to the current entity rotation via a quaternion multiplication. But Client B is not receiving the input for Client A and so this computation will always result in a null rotation.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635346537911_image.png)

So we need to do three things:

1. make sure that each client accumulate the correct angle for its own player entity in a graph variable and use that directly to drive the orientation
2. replicate this variable from each client to the server
3. broadcast the variable from the server to all the other clients

-we can use the *Set* and *Get float variable* nodes and reorganize our graph a bit to accomplish 1.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343525826_image.png)

-To solve 2, We then simply convert the *Set float variable* node in a *Float variable network replication* node, specifying the fact that only *clients* should set and replicate the variable using the *Network is of type* node.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635343619084_image.png)

>  **Note**: when you pass a null connection to the *network is of type* node you are implicitly asking the type of the “local” simulation.

3. is automatically done by the server: the moment it receives the variable update from the client it will automatically replicate the change to all the connected nodes. So we don’t have to do anything for this.

And now each client has the correct information about where each other client is looking at, and can animate the orientation of other players smoothly.