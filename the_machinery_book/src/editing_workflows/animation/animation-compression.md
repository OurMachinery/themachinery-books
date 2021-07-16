## Animation Compression

We support compressed animations. Compressed animations have the extension `.animation`. Note that with this, we have three kinds of animation resources:

| **Resource**      | **Description**                                              |
| ----------------- | ------------------------------------------------------------ |
| `.dcc_asset`      | Animation imported from a Digital Content Creation (DCC) software, such as Max, Maya, Blender, etc. Note  that `.dcc_asset` is used for all imported content, so it could be animations, textures, models, etc. |
| `.animation`      | A compressed animation. The compressed animation is generated from the `.dcc_asset` by explicitly compressing it. |
| `.animation_clip` | Specifies how an animation should be played: playback speed, whether it plays forward or backward, if it drives the root bone or not, etc.<br><br>An *Animation Clip* references either an uncompressed `.dcc_asset` or a compressed `.animation` to access the actual animation data. |

To create a compressed animation, right-click a `.dcc_asset` file that contains an animation and choose **Create xxx.animation** in the context menu:


![A compressed animation.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617123138052_image.png)


When you first do this, the animation shows a white skeleton in T-pose and a moving blue skeleton. The blue skeleton is the reference `.dcc_animation` and the white skeleton is the compressed animation. By comparing the skeletons you can see how big the error in the animation is.

At first, the white skeleton is in T-pose because we haven’t actually generated the compressed data yet. To do that, press the **Compress** button:


![Compressed animation with data.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617123319435_image.png)


This will update the **Format** and **Buffer** fields and we can see that we have 9.2 KB of compressed data for this animation and that the compression ratio is x 6.66. I.e, the compressed data is 6.66 times smaller than the uncompressed one. The white and the blue skeletons overlap. The compression error is too small to be noticed in this view, we have to really zoom in to see it:


![Zoomed in view of one of the fingers.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617123494752_image.png)


When you compress an animation like this, The Machinery tries to come up with some good default compression settings. The default settings work in a lot of cases, but they’re not perfect,
because The Machinery can’t know how the animation is intended to be viewed in your game.

Are you making a miniature fighting game, and all the models will be viewed from a distant overhead camera? In that case, you can get away with a lot of compression. Or are you animating a gun sight that will be held up really close to the player’s eye? In that case, a small error will be very visible.

To help the engine, you can create an `.animation_compression` asset. (**New Animation Compression** in the asset browser.) The Animation Compression asset control the settings for all the animations in the same folder or in its subfolders (unless the subfolders override with a local Animation Compression asset):


![Animation Compression settings.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617124020292_image.png)


 The Animation Compression settings object has two properties:

**Max Error** specifies the maximum allowed error in the compressed animation. The default value is 0.001 or 1 mm. This means that when we do the compression we allow bones to be off by 1 mm, but not more. The lower you set this value, the less compression you will get.

**Skin Size** specifies the size we assume for the character’s skin. It defaults to 0.1, or 10 cm. We need the skin size to estimate the effects of rotational errors. For example, if the rotation of a bone is off by 1°, the effect of that in mm depends on how far away from the bone the mesh is.

10 cm is a reasonable approximation for a human character, but notice that there are situations where the skin size can be significantly larger. For example, suppose that a 3 m long staff is attached to the player’s hand bone. In this case, rotational errors in the hand are amplified by the full length of the staff and can lead to really big errors in the position of the staff end. If this gives you trouble, you might want to up the skin size to 3 for animations with the staff.

We don’t support setting a per-bone skin size, because it’s unclear if the effort of specifying per-bone skin sizes is really worth it in terms of the memory savings it can give. (Also, even a per-bone skin size might not be enough to estimate errors perfectly. For example, an animator could have set up a miter joint where the extent of the skin depends on the relative angle of two bones and goes to infinity as the angle approaches zero.)

Note that sometimes animations are exported in other units than meters. In this case, the Skin Size and the Max Error should be specified in the same units that are used in the animation file.