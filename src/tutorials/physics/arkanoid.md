The Arkanoid scene shows you a physically accurate version of the famous Pong game.
The goal is to bounce the ball around and hit as many bricks as possible: the Bat can be controlled by moving the mouse left/right.

# **Arkanoid Scene breakdown**

## **Bat** (Prototype location: Special Objects/Bat.entity)

The Bat is the Entity that the player controls to hit the ball.
Relevant components:

- `Physics Shape`, to make the Bat collide with the ball and bounce it back.

  By examining the `Physics Shape` properties we can see that bot the Material and the Collision properties are set.

![](https://www.dropbox.com/s/mqprbsna9v3jlh3/image-20220311135902320.png?dl=1)

The Bouncy Material (`Physics Materials/Bouncy.physics_material`) has a Restitution Coefficient of 1. This is what makes the ball "bounce".

![image-20220311140003187](https://www.dropbox.com/s/5f93mvh8iaq828v/image-20220311140003187.png?dl=1)

The Bat Collision (`Physics Materials/Bat.physics_collision`) specifies the fact that shapes with this collision should only collide with entities that Have the `Default` Collision type. (Which can itself be found in the `Physics Materials` folder).
As you can imagine then, the Ball will have the Default collision set on its Shape.

![image-20220311140028100](https://www.dropbox.com/s/ow0v79qrk1hstvu/image-20220311140028100.png?dl=1)



- `Physics Body`, to make the Bat movement around the world Physically accurate.

  Examining the `Physics Body` properties, we notice that the `Kinematic` checkbox is flagged: this means that the position of the Bat Entity won't be driven by the Physics simulation itself, but that it will be driven by the position that is present in the transform component instead. In this case we'll alter the transform component position via the `Entity Graph` of the Bat: then the position of the `transform component` will be reflected automatically in the Physics simulation.

![image-20220311140100012](https://www.dropbox.com/s/twwcnz91jlrkv54/image-20220311140100012.png?dl=1)

- Entity Graph, which is used to:

  a) move the Bat via the mouse

  b) Push the ball in the opposite direction when the bat and the ball collides.

![image-20220311140128319](https://www.dropbox.com/s/oj6tsxdiua3wbb0/image-20220311140128319.png?dl=1)



> You may be wondering why it's not enough to just push the ball in the correct direction to make it bounce, and we have to set the restitution coefficient to 1 in addition to doing so.
> The answer is that if we leave the restitution coefficient to 0, the ball will loose all of its "energy" when it collides with the Bat, thus even if we later on push it in the correct direction it will still move very slowly.



## **Walls** (Prototype location: Shapes/Wall.entity)

The walls in the scene are just static Entities with a `Physic Shape` component and a scaled Box child Entity.
They're practially very similar to the Bat entity, just that they don't have:

- The `Physics body` component (we don't want walls to be able to move around).
- The `Entity Graph` component, as we don't need any logic applied to them: walls are just static entities.

![image-20220311140301191](https://www.dropbox.com/s/gycvtqu2vq4l1bo/image-20220311140301191.png?dl=1)



## **Bricks** (Prototype location: Special Objects/brick)

The "standard" brick (the one without a fancy blue ball on it) Is nothing more than a static Shape like walls are, with a small addition: we want bricks to be destroyed when they collide with the ball.

To accomplish that, they:

- Have the `Notify Touch` collision type, so that collisions with the ball are notified.
- Have an `Entity Graph` component that implements this very simple logic: they register the `Physx on contact event` and, once that triggers, they just delete themselves from the game by calling `destroy entity`.

![image-20220311140414076](https://www.dropbox.com/s/9v4veqzlx8qyxd5/image-20220311140414076.png?dl=1)



## **Special Bricks** (Prototype location: Special Objects/Multiball Brick.entity)

This special kind of brick works exactly like a standard brick, but with a simple addition: its `Entity Graph` is made so that when hit it will spawn an additional ball spawn in the game.

![image-20220311140520748](https://www.dropbox.com/s/c7gdhs5dtdzvhmh/image-20220311140520748.png?dl=1)

To see how it works, lets dive into his Entity Graph component, which is pretty similar to the standard brick's one.

In there we can see that, just after self-destroying itself, it will execute the `Spawn a new Ball` subgraph, which will simply spawn a new ball and push it.

![image-20220311140558642](https://www.dropbox.com/s/uchnbo0baqzljw6/image-20220311140558642.png?dl=1)



> Notice how we're using a `vec3` variable to store the position at which we want to spawn the additional ball in the `Save Position for New Ball` subgraph.



## **Lost ball trigger**

The Lost ball trigger is the Entity responsible for re-spawning the ball when it goes out of bounds.
The way it works is by having a `Physic Shape`  (you can see it in yellow by clicking on it in the Entity Tree) With the `Notify Touch` Collision type *and* with the `is_trigger` checkbox flagged:

![image-20220311140709526](https://www.dropbox.com/s/x3hzrnufansths4/image-20220311140709526.png?dl=1)



> Physics Shapes flagged with the `is_trigger` checkbox will still exists in the Physical world, but when a collision with them happen the collision will be notified but the objects will be allowed to "interpenetrate" with each other.

This means that it won't collide with the Ball (which has the Default collision, remember), and once the collision happens the `Physx On Trigger even`t will be triggered: (We can find it in the Entity Graph)

![image-20220311140758376](https://www.dropbox.com/s/vodlc8pohlz9xus/image-20220311140758376.png?dl=1)

Here we can see that once it's triggered, this event will:

- destroy the ball (Which is the _Touched_ entity, notice the difference between this trigger and the one in the Brick's graph: there we are deleting the brick itself)
- call the `Lost Ball` event on the parent entity (the parent entity is found via the Entity From Path Node specifying `..` as the path, which in this case is the Arkanoid Entity itself).

## **Arkanoid**

In addition to containing all the other entities as children, the Arkanoid entity also has the Entity Graph component that is used for Spawning a ball when the game starts (or when the ball goes out of bounds).

![image-20220311140926242](https://www.dropbox.com/s/0veudm4fv1zqoun/image-20220311140926242.png?dl=1)

You can see that the Spawn Ball event is called both at the beginning of the Game (When the Init event will be called) but also when a `Lost ball` event is triggered.

This concludes the tour of the Arkanoid scene, try to experiment it a bit and don't be scared of breaking stuff, you can always re-download the sample if you screw things up.