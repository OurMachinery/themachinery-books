# Overview of the Entity Context Lifecycle

This page describes the lifecycle of the entity context / the simulation and all its stages.

![](https://www.dropbox.com/s/vxq89spqcwzdvy8/tm_guide_ecs_life_cycle.png?dl=1)

## Update Phases

In your Engine / Systems you an define in which Phase of the Update loop, your Engine / System shall run. This can be managed via the:  `.before_me`, `.after_me` and `.phase`  fields of your engine or system definition. 

Please keep in mind that the Scheduler will order your system based on what kind of components you might modify or not! This is why it is always recommended to say what kind of components your system/engine will operate on and what they will do with them (Write to them or not). Depending on your dependencies the scheduler will decide if your engine/system can run in parallel.

**The Engine has default phases:**

| Name                  | When                                         |
| --------------------- | -------------------------------------------- |
| `TM_PHASE__ANIMATION` | Phase for animation jobs.                    |
| `TM_PHASE__PHYSICS`   | Phase for physics jobs.                      |
| `TM_PHASE__CAMERA`    | Phase for camera jobs.                       |
| `TM_PHASE__GRAPH`     | Phase for the visual scripting graph update. |
| `TM_PHASE__RENDER`    | Phase for render jobs.                       |

> **Note:** that phases are just string hashes and you can extend the systems with more phases if desired.