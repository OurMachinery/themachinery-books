## Animation

The *Animation* system lets you play animations on entities. You can also create complicated
animation blends, crossfades, and transitions using an *Animation State Machine*.

The animation system adds two new assets to The Machinery: *Animation Clip* and *Animation State
Machine* as well as two new components: *Animation Simple Player* and *Animation State Machine*.

To get an animation into *The Machinery* you first export it from your DCC tool as FBX or another
suitable file format. Then you import this using **File > Import...**.

An *Animation Clip* is an asset created from an imported DCC animation asset that adds some
additional data. First, you can set a range of the original animation to use for the clip, so you
can cut up a long animation into several individual clips. Second, you can specify whether the
animation should loop or not as well as its playback speed. You can use a negative playback speed to
get a "reverse" animation.

Finally, you can specify a "locomotion" node for the animation. If you do, the delta motion of that
node will be extracted from the animation and applied to the *entity* that animation is played on,
instead of to that bone. This lets an animation "drive" the entity and is useful for things like
walking and running animations. The locomotion node should typically be the root node of the
skeleton. If the root mode is animated and you "don't" specify a locomotion node, the result will be
that the root node "walks away" from the animation.

<iframe id="ytplayer" type="text/html" width="640" height="360"
  src="https://www.youtube.com/embed/OcgBaG0rHtk?autoplay=1"
  frameborder="0"></iframe>

The *Animation Simple Player Component* is a component that you can add to an entity to play
animations on it. The component lets you pick a single animation to play on the entity. This is
useful when you want to play simple animations such as doors opening, coins spinning, flags waving,
etc. If you want more control over the playback and be able to crossfade and blend between
animations you should use an *Animation State Machine* instead.
