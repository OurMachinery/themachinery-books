# Color Grading

The Machinery supports industry standard methods for color grading for HDR colors. Currently this is no support for custom tone mappers.

![Controls](https://www.dropbox.com/s/f51xt0yd696w3jv/tm_tut_color_grading_lgg_sop.png?dl=1)

The [Color Grading]({{docs}}plugins/default_render_pipe/color_grading.h.html) component allows you to use either Lift/Gamma/Gain controls or ASC-CDL controls, regardless of the method used, the shader will apply a single ASC-CDL transform per channel. The resulting transform is visualized using the graph. Color grading is applied just before the tone mapper in ACEScg space.

![](https://www.dropbox.com/s/xpl84f9l0mqbp1n/tm_tut_color_grading_flow.svg?dl=1)