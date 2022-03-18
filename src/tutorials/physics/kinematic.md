# Kinematic Scene breakdown

![image-20220317102629794](https://www.dropbox.com/s/jvy8da7ptkl5uk0/image-20220317102629794.png?dl=1)

## Plane

Just static geometry like we saw in previous scenes.

## Walls

Just static geometry. (Physics Shape component)

## Sweeper

The sweeper is a simple rigid body with a rectangular shape that will perpetually rotate on it's own Y axis.

The Rigid body component has the "Kinematic" flag set so that Physx knows that the position of the entity will be driven by its transform component.

The Velocity component is used to apply (in this case) a constant angular velocity to the entity to make it rotate on its own axis.

![image-20220318094033356](https://www.dropbox.com/s/timq3uy7mfltzfp/image-20220318094033356.png?dl=1)

## Spawners

There are four different spawners in the scene, placed at the four corners of the plane, and each one of them will spawn a physic object once every second.

Notice that the spawned entities won't have any force applied to them, so they will just fall on the ground. (Until they get swept by the Sweeper, I mean)

You can find the objects that will be spawned for each of the spawners under the Shapes folder. 

![image-20220317102210569](https://www.dropbox.com/s/elydub9tniba8a7/image-20220317102210569.png?dl=1)

## Ball Thrower (Prototype location: Special Objects/Ball Thrower)

The same ball thrower that we saw in the Contacts scene: press Space to throw a ball in the scene.
