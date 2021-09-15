# Color Grading

The Machinery supports industry standard methods for color grading for HDR colors. Currently this is no support for custom tone mappers.

![Controls](https://www.dropbox.com/s/f51xt0yd696w3jv/tm_tut_color_grading_lgg_sop.png?dl=1)

The [Color Grading]({{docs}}plugins/default_render_pipe/color_grading.h.html) component allows you to use either Lift/Gamma/Gain controls or ASC-CDL controls, regardless of the method used, the shader will apply a single ASC-CDL transform per channel. The resulting transform is visualized using the graph. Color grading is applied just before the tone mapper in ACEScg space.

![](https://www.dropbox.com/s/v8xm2u9ln0dy065/tm_tut_color_grading_flow.png?dl=1)

![](https://www.dropbox.com/s/9080y9197sr1p5v/tm_tut_color_grading_tools.png?dl=1)

The Color Scopes Tab can be used to visualize the color spread in your scene. This might aid in color grading. 