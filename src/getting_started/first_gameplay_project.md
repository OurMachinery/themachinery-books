# First Gameplay Project

This walkthrough shows how you make a simple scene via the Entity Graph.

This part will cover the following topics:

- How to create with the visual scripting language (The Entity Graph) a simple playable

**Table of Content**

* {:toc}

## How to add some life to your project

Let us create a new project and than add some gameplay to it. Before this, let us define a goal:
*This part aims to create a plane and a cube that we can move with W on this plane.*

It requires multiple steps:

- Add a plane to the Scene
- Add a box to the Scene
- Add a camera
- Make the box and the plane physical so the box cannot fall through
- Add an Entity graph for the movement

The first one is to add a plane to our Scene. As we remember in *Core* in the folder *geometry*, we have a plane entity. All we need to do is drag it into the Scene and scale it a bit up.

![Open the core/geometry folder and add the plane.entity to the scene by dragging it into the scene](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615459641040_add_plane.gif)


The next step is as straightforward as the first step. We repeat what we did before and drag and drop the box from the geometry folder into the scene tab. After this, we can see what happens in the simulation. To start the simulation and open the simulation tab, you need to click on the "play" button.


![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615460126086_image.png)


The moment the simulation tab opens, the simulation starts. As you might have guessed, nothing happens. You can navigate in the tab by using the AWSD keys if no custom camera is selected. Also, we can pause, reset the current simulation or increase the simulation speed.

![Pause, reset and increase simulation speed](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615460267868_image.png)


Let us go back to the scene tab and add some more exciting things. The next point of our task list is to add physics. To make our entities aware of physics, we need to add the Physics Shape and Physics Body Component to the corresponding entities. 
In this case, the plane should have the Physics shape component that we set as a plane shape, and the box should have the physics shape component and the physics body component. 
Adding a component to an entity can be done either through right-click on and then **Add Component** via the Entity tree or the property tab and the Add component button. It is also possible to select an entity in the Entity Tree and use Space.

![box entity](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615461868389_image.png)
![plane entity](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615461884406_image.png)


To visualize the box shape or the plane shape, we can use the visualization menu in either the scene or simulation tab.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615462081977_image.png)


When the simulation starts, the box - if placed above the plane - will fall on the plane. Isn't this already more exciting?


## Add some movement

The next step is to make the box move. There are two approaches we could do a physicals-based movement or just a placement change. We are starting with the simpler option: Placement Change.

We need to add Graph Component to the box entity. (We could also add it to any other entity or the world entity, but we add it to the box for simplicity and organization's sake add it to the box).

![Add Menu opened via right click “Add Component”](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615462362939_image.png)


When the Graph component has been added, all we need is to double-click the Component, and the Graph Editor opens.


![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615462398554_image.png)


The Graph Editor View is empty. We can add new nodes via pressing Space or right-click a new node. It opens the node adding a menu. In there, we can search for nodes.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615462451823_image.png)


The Entity Graph is an event-based Visual Scripting Language. It means events will trigger actions. 

There are three main events we should use for a particular type of action:

- Init Event - This gets called when the Graph component gets initialized. The perfect place to set up variables etc.
- Tick Event - For all actions that need to happen on Tick (Be aware that this might influence your game performance if you do expensive things always on tick)
- Terminate Event - For all actions that need to happen when the Component gets removed. It mainly happens when the Entity gets destroyed.

You can also create custom events and listen to them. You can define those events in the graph itself or in C.

Our first iteration will use changing the placement of our box whenever we use the key `W`. The Machinery input system is based on polling rather than on events. 
We can check if key was pressed via the "Key Poll" node needs to be checked every frame. Therefore a tick event is a need. The "Key Poll" node requires the specify the key and returns a Boolean (true/false) if a key has been pressed, is down, released, or up.
It leads to the following setup:

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615463509298_image.png)


In this setup on tick, it's being checked if the key "w" is down. If that is the case, the graph will execute the logic. 

What is the actual logic? The actual logic is 

1. to get the Entity
2. get its transform
3. get the components of the transform (split the vector in x,y,z)
4. manipulate the x value
5. set the new transform to the Entity

In the Entity Graph, any entity of the current Scene can be referenced by name. It 
happens via the "Scene Entity" node. 

> If no name is provided, it will return the graph components Entity.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615463752914_image.png)


The return type is an Entity. When we drag the wire into the void, the Add Node menu will suggest only nodes which take the Entity as input:

![With expanded Entity Category](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615463814348_image.png)


We should connect the entity wire with a Get Transform node to get the world transform. Then the transform position should be split into its components. After this, component X should be modified by adding 10 * delta time.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615463996352_image.png)


To get the delta time, all that is needed is to add the delta time node and multiple its float value with 10.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615464050098_image.png)


When all this is complete, we should set the position of the Entity to the new value. First, a new position vector needs to be constructed by adding the old values to it and then the new modified value.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615464121876_image.png)


The next step is to tell the Entity to use this position instead of the old one. This happens through the Set Transform node.

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615464271230_image.png)

> Note that we leave all the other things as they were. It means they remain as before the change.

If we simulate the Scene now, the box moves, but it won't fall into the void if we move it to beyond the plane. It was to be expected because the physics system has not been updated, and therefore the velocity has not changed.


## Add physics-based movement

To make the box move with the physics system, we can use the node "PhysX Push":

![](https://paper-attachments.dropbox.com/s_09462F237550F87F4C86951FAA779F713337E632E917FE6E6B8E3406BD58F125_1615465150791_image.png)


The node will move the box by applying velocity to it.


## What is next?

If you are more interested in physics, download the physics sample via the download tab in that project, you will learn more about the use of physics in the Engine.

