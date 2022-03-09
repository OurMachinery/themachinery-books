# Part 1: Network Assets 

In this tutorial you’ll learn how to create new Network Node Assets.

>  **Note:**  we start with making sure that you have the Networking feature flag enabled, you can do that in the **Tools→Feature Flags Menu**. 

## Video
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/nKglvZ8og1w?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Tutorial
In The Machinery, every simulation instance is separated from each other: the simulation that runs in the Simulate Tab, for example, is completely different from the simulation that runs on the Preview Tab, and they Cannot talk to each other: The goal of the Networking layer in The Machinery is to allow different Simulations to send data to each other.

To do that, we introduced a specific type of asset that defines how a specific kind of simulation (Client, Server, Etc) should behave with regards to the other nodes that there are on the Network: The Network Node.

To define a Network Node Asset, go in the asset browser, right click and select New→New Network Node.

Let’s define a Server network Node and a Client Network Node so that we can use them in our project:

### Server

We want the server to be able to receive packets from other nodes, so let’s bind the default Simulation Receiver interface in the Properties view.

We also want our Server to Accept incoming connections from other Nodes. For now we’ll bind the “Accept From everyone” Accept interface, meaning that the server will accept connections from everyone.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635338868858_image.png)

### Client

Our Client will need to accept connections from the Server (In The Machinery the concept of “connection” is unilateral, so the Client will open a connection to the Server but in turn the Server will open a connection in the opposite direction) so let’s bind the “Accept from everyone” accept interface as well.

The Client will also need to receive packets (the updates to the Gamestate that come from the Server), so make sure to bind the default simulation receiver to the Client as well.

We want our Client to immediately connect to the Server when it’s started: let’s bind the “Connect to local Server” bootstrap interface. (It will run immediately after the Client instance is created)

We also know that our Server will send Gamestate updates to our Client: so we want the Client to start with an empty world, assuming that all the necessary updates will later come from the Server. For this reason, make sure to toggle the “passive Gamestate” flag on the Client asset.

![img](https://paper-attachments.dropbox.com/s_5F8ED61A9C68BDE8B9368D5E3DABD345E39CC324FB030EDE9E31314C3B7EE30F_1635342631803_image.png)

 