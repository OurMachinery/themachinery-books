# Contacts scene breakdown

![image-20220318094339252](https://www.dropbox.com/s/s2ocyt0bcywxjkl/image-20220318094339252.png?raw=1)

## Plane

The Plane Entity is just a simple Entity with a Shape attached to it.



## Spawn Pile

The Spawn Pile doesn't have any Physics component attached to it, but its Entity Graph will spawn a new Box every Three seconds and Push it down towards the Ground.

![image-20220317093117838](https://www.dropbox.com/s/pn0mnz7l1vcac8u/image-20220317093117838.png?raw=1)



## Ball thrower (Prototype location: Special Objects/Ball Thrower)

The Ball Thrower doesn't have any Physics component either, but it will spawn a new ball in the viewing direction if the spacebar is pressed. The Logic is pretty similar to the one of the Spawn Pile: Spawn a new entity and use the Physx Push Node to push it in a specific direction, in this case the camera viewing direction.

![image-20220317093549002](https://www.dropbox.com/s/yxmcg9znvubo4jp/image-20220317093549002.png?raw=1)



That's it for the Contacts scene, it's a pretty simple one.

You will notice that the Boxes only collide with the blue spheres and the Ground plane: as an exercise try to make it so that the boxes also collides with each other.