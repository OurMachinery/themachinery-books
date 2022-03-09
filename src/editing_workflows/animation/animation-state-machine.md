### Animation state machines

The *Animation State Machine Asset* represents an *Animation State Machine*. If you double-click an
Animation State Machine Asset in the Asset Browser, an Animation State Machine Editor will open:

![Animation State Machine Editor](#)

The Animation State Machine (ASM) introduces a number of concepts: *Layers*, *States*,
*Transitions*, *Events*, *Variables*, and *Blend Sets*.

The ASM represents a complex animation setup with multiple animations that can be played on a
character by dividing it into *States*. Each state represents something the character is doing
(running, walking, swimming, jumping, etc) and in each state, one particular animation, or a
particular blend of animations is being played. The states are the boxes in the *State Graph*.

The ASM can change state by taking a *Transition* from one state to another. The transitions are
represented by arrows in the graph. When the transition is taken, the animation crossfades over from
the animations in one state to the animations in the other state. The properties of the transition
specify the crossfade time. Note that even though the crossfade takes some time, the logical *state
transition* is immediate. I.e. as soon as the transition is taken, the state machine will logically
be in the new state.

The transitions are triggered by *Events*. An event is simply a named thing that can be sent to the
ASM from gameplay code. For example, the gameplay may send a "jump" event and that triggers the
animation to transition to the "jump" state.

*Variables* are float values that can be set from gameplay code to affect how the animations play.
The variables can be used in the states to affect their playback. For example, you may create a
variable called `run_speed` and set the playback *Speed* of your *run* state to be `run_speed`.
That way, gameplay can control the speed of the animation.

Note that the *Speed* of a state can be set to a fixed number, a variable, or a mathematical
expression using variables and numbers. (E.g. `run_speed * 2`.) We have a small expression language
that we use to evaluate these expressions.

The ASM supports multiple *Layers* of state graphs. This works similar to image layering in an
application such as Photoshop. Animations in "higher" layers will be played "on top" of animations
in the lower layers and hide them.

As an example of how to use layering, you could have a bottom layer that controls the player's basic
locomotion (walking, running, etc). Then you could have a second layer on top of that for
controlling arm movements. That way, you could play a reload animation on the arms while the legs
are still running. Finally, you could have a top layer to play "hurt" animations when the player for
example gets hit by a bullet. These hurt animations could then interrupt the reload animations
whenever the player got hit.

*Blend Sets* can be used to control the per-bone opacity of animations playing in higher layers.
They simply specify a weight for each bone. In the example above, the animations in the "arm
movement" layer would have opacity 1.0 for all arm bones, but 0.0 for all leg bones. That way, they
would hide the arm movement from the running animation below, but let the leg movement show through.

The Animation State Machine Editor has a *Tree View* to the left that lets you browse all the
layers, states, transitions, events, variables, and blend sets. The *State Graph* lets you edit the
states and transitions in the current layer. The *Properties* window lets you set the properties of
the currently selected objects and the *Preview* shows you a preview of what the animation looks
like. Note that for the preview to work, you must specify a *Preview Entity* in the properties of
the state machine. This is the entity that will be used to preview the ASM. When you select a state
in the *State Graph*, the preview will update to show that state.

In the *Preview* window, you also find the *Motion Mixer*. This allows you to send events to the ASM
and change variables to see how the animation reacts.

The ASM currently supports the following animation states:

**Regular State**

Plays a regular animation.

**Random State**

Randomly plays an animation out of a set of options.

**Empty State**

A state that doesn't play any animation at all. Note that this state is only useful in higher layers.
You can transition to an empty state to "clear" the animation in the layer and let the animations from
the layers below it shine through.

**Blend State**

Allows you to make a 1D or 2D blend between animations based on the value of variables. This is often
used for locomotion. You can use different animations based on the characters running speed and whether
the character is turning left or right and position them on a map to blend between them.

![Animation Blending](#)

Once you have created an Animation State Machine, you can assign it to a character by giving it an
Animation State Machine Component.

For an example of how the animation system works, have a look at the `mannequin` sample project.

### Missing features

Note that the animation system is still under active development. Here are some features that are
planned for the near future:

* Ragdolls.
* Animation compression.
* Triggers.
* More animation states.
  * Offset State.
  * Template State.
  * Expression-based Blend State.
  * Graph-based Blend State.
* Beat transitions.
* Constraints.
