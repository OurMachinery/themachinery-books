## Physics

The Machinery integrates Nvidia's PhysX toolkit and uses it for physics simulation of entities. This
section will not attempt to describe in detail how physics simulation works, for that we refer to
[the PhysX documentation](https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/guide/Manual/Index.html). We will only talk about how physics is set up in The Machinery.

The physics simulation system introduces two new assets: *Physics Material* and *Physics Collision*
as well as four new components: *Physics Shape Component*, *Physics Body Component*, *Physics
Joint Component*, and *Physics Mover Component*.

A *Physics Material* asset specifies the physical properties of a physics object: *friction* (how
"slippery" the object is) and *restitution* (how "bouncy" the object is). Note that if you don't
assign a material to a physics shape it will get default values for *friction* and *constitution*.

A *Physics Collision* asset describes a *collision class*. *Collision Classes* control which physics
shapes collide with each other. For example, a common thing to do is to have a *debris* class for
small objects and set it up so that *debris* collide with regular objects, but not with other
*debris*. That way, you are not wasting resources on computing collisions between lots of tiny
objects. (Note that the debris objects still need to collide with regular objects, or they would
just fall through the world.)

In addition to deciding who collides with who, the collision class also decides which collisions
generate callback events. These events can be handled in the *Entity Graph*.

If you don't assign a collision class to a physics shape, it will get the *Default* collision class.

The *Physics Shape Component* can be added to an entity to give it a collision shape for physics.
Entities with shape components will collide with each other when physics is simulated.

A physics shape can either be specified as geometry (sphere, capsule, plane, box) or it can be
computed from a graphics mesh (convex, mesh). Note that if you use computed geometry, you must press
the **Cook** button in the Properties UI to explicitly compute the geometry for the object.

![Convex shape.](https://www.dropbox.com/s/v5jnthc50vsa1oi/convex-physics-shape.png?dl=1)

If you just give an entity a *Physics Shape Component* it will become a static physics object. Other
moving objects can still collide with it, but the object itself won't move.

To create a moving physics object, you need to add a *Physics Body Component*. The body component
lets you specify dynamic properties such as damping, mass, and inertia tensor. It also lets you
specify whether the object should be *kinematic* or not. A *kinematic* object is being moved by
*animation*. Its movement is not affected by physics, but it can still affect other physical
objects by colliding with them and pushing them around. In contrast, if the object is *not
kinematic* it will be completely controlled by physics. If you place it above ground, it will fall
down as soon as you start the simulation.

Note that parameters such as *damping* and *mass* do not really affect kinematic objects, since
the animations will move them the same way, regardless of their mass or damping. However, these
parameters can still be important because gameplay code could at some point change the object
from being kinematic to non-kinematic. If the gameplay code never makes the body non-kinematic, the
mass doesn't matter.

The *Physics Joint Component* can be used to add *joints* to the physics simulation. Joints can tie
together physics bodies in various ways. For example, if you tie together two bodies with a hinge
joint they will swing as if they were connected by a hinge. For a more thorough description of
joints, we refer to the PhysX documentation.

The *Physics Mover Component* implements a physics-based character controller. If you add it to an
entity, it will keep the entity's feet on the ground, prevent it from going through walls, etc. For
an example of how to use the character controller, check out the `animation` or `gameplay` sample
projects.

Note that The Machinery doesn't currently support all the features found in PhysX. The most
glaring omissions are:

* D6 joints and joint motors.
* Vehicles.

We will add more support going forward.

For an example of how to use physics, see the `physics` sample project.

### Physics scripting

Physics can be scripted using the visual scripting language in the *Entity Graph*.

We can divide the PhysX scripting nodes into a few categories.

**Nodes that query the state of a physics body:**

- Get Angular Velocity
- Get Velocity
- Is Joint Broken
- Is Kinematic

**Nodes that manipulate physics bodies:**

- Add Force
- Add Torque
- Break Joint
- Push
- Set Angular Velocity
- Set Kinematic
- Set Velocity

**Event nodes that get triggered when something happens in the scene:**

- On Contact Event
- On Joint Break Event
- On Trigger Event

**Nodes that query the world for physics bodies:**

- Overlap
- Raycast
- Sweep

Note that the query nodes may return more than one result. They will do that by triggering their
*Out* event multiple times, each time with one of the result objects. (In the future we might change
this and have the nodes actually return arrays of objects.)
