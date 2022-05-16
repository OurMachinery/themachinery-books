## Triggers

This walkthrough shows you how to create a trigger with the Graph Component. You can find the "source code" in our [Physic Samples](https://ourmachinery.com/samples.html).

**Table of Content**

* {:toc}

## Assemble a Trigger

What is a trigger? 

Something that reacts when something intersects/touches them, either constantly or just the first/last time.



> **Note:** In Unreal Engine, this might be called Trigger Actors / Trigger Box. 



In the Machinery, we have two types of triggers we can use:

- PhysX's Trigger- Physical Based Trigger
- Volume-Component - The Trigger is based on the Volume Component.

In this walkthrough, we are focused on **PhysX's Trigger** **Event.**



This walkthrough will be to create a Trigger that adds Velocity to a Ball Shot from the Camera. Therefore we need to make the following Entities:

- The Trigger
- A world (plane)
- A Ball



### Create the Trigger Entity

Let us create a folder in the Project root and call it "Special Objects". It will be the folder in which we keep all our *Special Objects* for now and for what might come.

In this folder, we create an Entity with the name "Trigger". We add two extra components:

- A Graph Component for some logic
- A Physic Shape to make sure the Physics World can see it

When adding the Physic Shape, we need to consider the Type. By default, the Type is Sphere, but that would not suit our needs since we want it to be a red box. We change the Type to Box and tick the Checkbox "Is Trigger" to make sure it is a Trigger. We can also change the Half Extent value if we like.

If you look now into the Scene Tab, you see nothing. To change that, you can turn on the Debug Visualization:

![](https://www.dropbox.com/s/jp8oxoz8zl0f5d7/tm_tut_physics_viz.png?raw=1)

Having a Trigger that cannot be seen might be applicable for some games. In our case, we choose to make the Trigger Visible with a box.

Luckily the core provides a Box Entity for us: `core/geometry/box.entity`. 

![](https://www.dropbox.com/s/xd9gjg8pbw6p8kj/tm_tut_physics_core_gom.png?raw=1)

This location is something we keep in mind!

Let us also add the Box (`core/geometry/box.entity`) from the core to our Entity as a child. This Box makes it easier for us to test it later because we can see it in the Scene Window.


###  Add the logic to the graph

We double-click the Graph Component to open the Graph Editor. The Graph Editor is Empty. We want to add an `Init Event` and then a "Physx On Trigger Event". We need to connect the Start Listing connector with the "Init Event Connector".

To get the current Entity, we add the node "Scene Entity" and connect the outgoing connector with the "Physx On Trigger Event" Entity connector. 

The goal was to apply Velocity to any entity that touches the Trigger the first time. That is why we add a connector from the "First Touch" to the newly added Physx Set Velocity node.

We connect the Entity from the "Physx Set Velocity" entity connector to the *Touched Entity Connector* at the "Physx On Trigger Event" node. 

We need to get the current Velocity of this Entity. We can do this by using the "Physx Get Velocity" node. The result we modify with, let us say -1 and apply it at the end. (*The lower the value, the stronger the ball will bounce off.*)

![](https://www.dropbox.com/s/g8yhrs5e7wugau4/tm_tut_physics_graph_trigger_event.png?raw=1)


This is how our trigger Entity looks like:

![](https://www.dropbox.com/s/njipx8mfsjsqcgj/tm_tut_physics_trigger_entity.png?raw=1)

> **Note:** The Box Entity will be displayed yellow because it is a prototype instance of the Entity within the `core/geometry/` folder. Any changes to this prototype will apply to this instance as well. 


### Create the ball

The Trigger is quite useless unless it can interact with something! That is why we want to shoot a ball from the Camera to the player.

Again the core comes to our rescue and provides us with a Sphere in the `core/geometry/`! We will use this for our ball!



We open the "Special Objects" folder and add a new Entity called "Ball". With a double-click, we open it and add a "Physics Shape" and "Physics Body" Component. In the  "Physics Shape Component," we leave the Type to Sphere. 



> **Note:** We can also visualize the Sphere Physics Shape in the Scene the same way we visualized them for the Box.



After this, we need to ensure that our ball has Continuous Collision Detection (CCD) enabled. Also, the Inertia Tensor should be set to 0.4, and Angular Damping should be set to 0.05.



Now that we have adjusted all the components let us add the actual ball. Again we can drag and drop the `sphere.entity` from the `core/geometry/` folder onto our Entity.

![](https://www.dropbox.com/s/xd9gjg8pbw6p8kj/tm_tut_physics_core_gom.png?raw=1)



### Creating the Scene

After we have nearly all the components to create our little Scene, all that is missing is the playground. The playground can be defined as just a plane with a trigger on it.



We can create a new Folder in the Asset Browser root and call it "Scenes". In there, we create a new Entity and call it "Triggers". We open this Entity.

The first thing we do is add a new Empty Child entity. We call it Floor or Plane. 



>  **Note:** Right-click on the Main Entity "Add Child Entity."



We add a Physics Shape Component to this Entity and change its Type to Plane.

If we do not use the Physics Visualization mode, we see nothing in the Scene Tab. We can change this by adding a new Child Entity to our floor Entity. We right-click on the Plane / Floor Entity **->Add Child Entity -> From Asset**, and we search for the Plane Entity. It is also located in the core.



When we look at the Scene Tab now, we see our new floor entity! Let us drag in our Trigger. We need to drag and drop the Trigger Entity from the Asset Browser in the Scene and adjust it with the Tools within the Scene Tab.

The result could look like this:

![](https://www.dropbox.com/s/w4xqxvhcblinopu/tm_tut_physics_trigger_scene.png?raw=1)



>  **Note:** We should add a Light Entity. Otherwise, it might be quite dark. Luckily the core has our back also here. We can just right-click the main Entity and **Add Child Entity -> From Asset -> Light**.



### Spawn balls

The Scene itself is not what we want because we cannot spawn balls yet. To do this, we add a graph to the Scene itself.

In there, we add a "Tick Event" we need to poll every tick if the space key has was pressed. If you pressed space, we would spawn the ball from the camera direction. 

We push the ball via "Physx Push" with a calculated velocity.

![](https://www.dropbox.com/s/q9k4qp08lumgzef/tm_tut_physics_graph_spawn_ball.png?raw=1)



## Conclusion

All of the above described "code you can" find when you download the Physics Sample projects from the Download Tab: ***Help -> Download Sample Projects*** 
