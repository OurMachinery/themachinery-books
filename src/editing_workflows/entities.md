## Entities

*The Machinery* uses an entity-component based approach as a flexible way of
representing “objects” living in a “world”.

An *entity* is an independently existing object. An entity can have a number of
*components* associated with it. These components provide the entity with
specific functionality and features. The components currently available in *The*
*Machinery* are:

| Component                             | Description                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| **Animation&nbsp;Simple&nbsp;Player** | Plays individual animations on the entity.                   |
| **Animation&nbsp;State&nbsp;Machine** | Assigns an Animation State Machine to the entity which can be used to play and blend between animations. |
| **Camera**                            | Adds a camera to the entity. The **Scene > Camera** menu option lets you view the scene through this camera. |
| **Cubemap&nbsp;Capture**              | Used to capture cubemaps to be used for rendering reflections. |
| **Dcc&nbsp;Asset**                    | Renders an asset from a DCC tool. For more advanced rendering you would use the *Render* component. |
| **Entity&nbsp;Rigger**                | Used to "rig" an imported DCC Asset as an entity. See below. |
| **Graph**                             | Implements a visual scripting language that can be used to script entity behaviors without writing code. |
| **Light**                             | Adds a light source to the entity.                           |
| **Physics&nbsp;Body**                 | Represents a dynamic physics body. Entities that have this component will be affected by gravity. |
| **Physics&nbsp;Joint**                | Represents a physics joint, such as a hinge or a ball bearing. |
| **Physics&nbsp;Mover**                | Represents a physics character controller. Used to move a character around the physics world. |
| **Physics&nbsp;Shape**                | Represents a physics collision shape. If the entity has a physics body, this will be a dynamic shape, otherwise a static shape. |
| **Render**                            | Renders models output by a Creation Graph.                   |
| **Scene&nbsp;Tree**                   | Represents a hierarchy of nodes/bones inside an entity. Entities with skeletons, such as characters have scene trees. |
| **Sculpt**                            | Component used to free-form sculpt with blocks.              |
| **Sound Source**                      | Component that will play a looping sound on the entity.      |
| **Spin**                              | Sample component that spins the entity.                      |
| **Tag**                               | Assigns one or more "tags" to an entity, such as "bullet", "player", "enemy", etc. When implementing gameplay, we can query for all entities with a certain tag. |
| **Tessellated&nbsp;Plane**            | Sample component that draws a tessellated plane.             |
| **Transform**                         | Represents the entity’s location in the world (position, scale, rotation). Any entity that exists at a specific location in the world should have a Transform Component. Note that you can have entities without a Transform Component. Such entities can for example be used to represent abstract logical concepts. |
| **Velocity**                          | Gives the entity a velocity that moves it through the world. |

In addition to components, an entity can also have *Child Entities*. These are
associated entities that are spawned together with the entity. Using child
entities, you can create complex entities with deep hierarchies. For example, a
house could be represented as an entity with doors and windows as child
entities. The door could in turn have a handle as a child entity.

In *The Machinery* entity system, an entity can't have multiple components of the same type. So you
can’t for example create an entity with two Transform Components. This is to avoid confusion
because if you allowed multiple Transform Components it would be tricky to know which represented
the “actual” transform of the entity.

In cases where you want multiple components (for example, you may want an entity
with multiple lights) you have to solve it by creating child entities and have
each child entity hold one of the lights.

> Note that *The Machinery* does not have specific *Scene* assets. A scene in The
> Machinery is just an entity with a lot of child entities.
