# Build Custom UI Controls, Part I

Hi, we are starting a 3-part tutorial series about The Machinery UI system. In Part I, we’ll talk about the basics and create a custom circular button. In Part II, we’ll create a custom button with textures support. To show the results of the first two parts, we’ll be using a simple custom tab, so in Part III, we’ll see how to set up your UI and render it on screen.

During this tutorial, you’ll implement the `tm_ui_custom_controls` plugin, which will contain the `tm_ui_custom_controls_api` for draw custom controls in UI and `tm_ui_custom_controls_tab` custom tab in order to visualize results in a separate tab.

**Table of Content**

* auto-gen TOC;
{:toc}

## Environment setup

During this tutorial, you’ll build the `tm_ui_custom_controls` plugin, which will contain the `tm_ui_custom_controls_api` for draw custom controls and `tm_ui_custom_controls_tab` custom tab in order to visualize results in a separate tab.
> The source code is hosted on [https://github.com/raphael-ourmachinery/tm-custom-control-tutorial](https://github.com/raphael-ourmachinery/tm-custom-control-tutorial), copy the contents of `skel/` folder to a separate directory, the final result will be available in `part1/` folder. 

Below is a list of files of our project:

- `skel/libs.json`: specify premake5 binaries that will be downloaded from The Machinery server;
- `skel/(premake5.lua/build.bat/build.sh)`: build scripts that use `tmbuild.exe` to build our shared library. Note that we are targeting `TM_SDK_DIR/bin/plugins`, so our plugin will be automatically loaded by the engine. You’ll need to set the `TM_SDK_DIR` environment variable pointing to The Machinery directory. 
- `skel/src/custom_tab.(c/h)`: this is a minimal version of the custom tab sample, which makes it easier to see our custom button;
- `skel/src/ui_custom_controls_loader.(c/h)`: load the necessary APIs, it contains the definition of `tm_load_plugin()` needed our plugin be loaded by the plugins system;
- `skel/src/ui_custom_controls.(c/h)`: implementation of our circular button, later you can extend the API with your custom controls too.

## Circular Custom Button:

The Machinery uses an immediate-mode UI. You can read more about it on [One Draw Call UI](https://ourmachinery.com/post/one-draw-call-ui/) blog post. To draw 2D shapes, we’ll be using the [`tm_draw2d_api`]({{docs}}plugins/ui/draw2d.h.html#structtm_draw2d_api) implemented in [`draw2d.h`]({{docs}}plugins/ui/draw2d.h.html), which supplies functions to draw basic 2D shapes. As we are implementing a circular button, we’ll we need to draw a circle using the following function:


    tm_draw2d_api→fill_circle(tm_draw2d_vbuffer_t *vbuffer, tm_draw2d_ibuffer_t *ibuffer, const tm_draw2d_style_t *style, tm_vec2_t pos, float radius)

You can note this function takes a vertex and an index buffer as arguments. In the following tutorials, we’ll learn more about it, but for now, you only need to know is that [`tm_draw2d_api`]({{docs}}plugins/ui/draw2d.h.html#structtm_draw2d_api) will fill them, and we need to call [`tm_ui_api->buffers()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.buffers()) to get the buffers. Later the engine will use [`tm_ui_renderer_api`]({{docs}}plugins/ui/ui_renderer.h.html#structtm_ui_renderer_api) to draw the UI using one draw call.

Let’s add some more information `tm_ui_circular_button_t` and use it on `circular_button()`:


- ui_custom_controls.h:

```C
    ...
    
    typedef struct tm_ui_circular_button_t
    {
        uint64_t id;
    
        tm_vec2_t center;
        float radius;
        tm_color_srgb_t background_color;
    } tm_ui_circular_button_t;
    
    ...
```


- ui_custom_controls.c:

```C
    ...
    
    bool circular_button(struct tm_ui_o *ui, const struct tm_ui_style_t *uistyle, const tm_ui_circular_button_t *c)
    {
        // tm_ui_buffer_t contains information needed when creating a custom control
        tm_ui_buffers_t uib = tm_ui_api->buffers(ui);
    
        // convert tm_ui_style_t to tm_draw2d_style_t
        tm_draw2d_style_t style;
        tm_ui_api->to_draw_style(ui, &style, uistyle);
        style.color = c->background_color;
    
        tm_draw2d_api->fill_circle(uib.vbuffer, uib.ibuffers[uistyle->buffer], &style, c->center, c->radius);
    
        return false;
    }
    
    ...
```

For control interaction logic, we'll need interfaces from [`ui_custom.h`]({{docs}}plugins/ui/ui_custom.h.html#ui_custom.h), actually all editor's UI is implemented using them.  [`tm_ui_buffers_t`]({{docs}}plugins/ui/ui.h.html#structtm_ui_buffers_t) that we got earlier has two important members, [`tm_ui_activation_t`]({{docs}}plugins/ui/ui_custom.h.html#structtm_ui_activation_t) one keeps the information about activation and hovering state of UI controls, and [`tm_ui_input_state_t`]({{docs}}plugins/ui/ui_custom.h.html#structtm_ui_input_state_t) maintains the input state. The table below lists some important concepts of our UI system. You can read it at once, or skip for now and return when necessary:

| **Concept**      | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                  |
| ID               | Each control in the UI has a unique 64-bit identifier. Since controls are not explicitly created and destroyed, the ID is the only thing that identifies a control from one frame to the next.<br><br>You create a new ID by calling [`tm_ui_api->make_id()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.make_id()). IDs are assigned sequentially by the UI. You have to be a bit careful with this if you have controls that sometimes are visible and sometimes not, such as *context menus*. If you only generate the ID for the context menu when it is visible, it will change the numbering of the subsequent controls depending on whether the menu is visible or not. Since controls are identified by their IDs, this can lead to controls being misidentified.<br><br>A good strategy is to generate the IDs for all the controls that you *might* show upfront, so that the ID assignment is stable.<br><br>Note: We may change this in the future if we can find a more stable way of assigning IDs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Hover            | The UI system keeps track of which control the mouse pointer is *hovering* over, by storing its ID in a *hover* variable.<br><br>You never set the *hover* variable directly. Instead, in your control’s update, you check if the mouse is over your control with [`tm_ui_api->is_hovering()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.is_hovering()), and if it is you set `next_hover` to its ID. At the end of the frame, the UI assigns the value of `next_hover` to the `hover` variable.<br><br>The reason for this two-step process is that multiple controls or objects might be drawn on top of each other in the same area of the UI. The last object drawn will be on top and we want the *hover* variable to reflect whatever the user sees on the screen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Overlay          | The UI is actually drawn in two layers, one *Base* and one *Overlay* layer. The controls in the overlay layer are drawn on top of the controls in the *Base* layer, even if they are drawn earlier in the draw order. We use the Overlay layer for things like drop-down menus that should appear on top of other controls.<br><br>If an earlier control set *next_hover* to a control in the Overlay layer, this shouldn’t be changed by a later control in the base layer, because the Overlay layer control will appear on top of that one. We use a variable `next_hover_in_overlay` to keep track of if the current `next_hover` value represents an ID in the Overlay layer. In this case, it shouldn’t be changed by base layer controls.<br><br>In practice, the Overlay layer is implemented by keeping track of two index buffers in the drawing system, one for the base layer and one for the overlay layer. (Note that the two layers still share a single vertex buffer.) At the end of drawing, we merge the two buffers into one, by simply concatenating the Overlay buffer at the end of the base Buffer, thus making sure the overlay controls are drawn later, on top of the base control. With this approach, we can still draw everything with a single draw call.<br><br>Note that as a consequence of how we render our UI — we only have a single Vulkan context and everything is drawn with the same draw call — drop-down menus and other pop-up controls cannot extrude past the edges of the system window — everything is drawn with the system window rect.                                                                                                                                                                                                                                                                       |
| Active           | Similar to *Hover*, *Active* is a variable that keeps track of the currently active control, i.e. the control the user is currently interacting with.<br><br>We need to keep track of the active control for two reasons. First, we often want to draw the active control in a special way, such as showing a highlight and a caret in an active text box.<br><br>Second, the active control typically needs to keep track of some extra state. For example, an active slider needs to keep track of the slider’s initial position so that it can pop back to that if the user drags the mouse outside the slider.<br><br>The UI system uses a single large `char[]` buffer to keep track of the current active control’s state. This buffer is shared by all controls. Since there can only be one active control at a time, only one control will be using this buffer at a time. When a new control becomes active the buffer is zeroed (this should be a valid initial state for the active data).<br><br>Typically a control becomes active if the user presses the left mouse button while the control is being *hovered*. In this case, the control will call [`tm_ui_api->set_active()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.set_active()). Though there are other ways a control can become active too, such as by tabbing. To implement tab focus, you need to call [`tm_ui_api->focus_on_tab()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.focus_on_tab()) in the control’s code.                                                                                                                                                                                                                                                                                                                                                                                         |
| Clipping         | The drawing system has support for *Clipping* *Rects.* This is mostly useful when you need to clip text to a control’s rect. You create a new clipping rect by calling [`tm_draw2d_api->add_clip_rect()`]({{docs}}plugins/ui/draw2d.h.html#structtm_draw2d_api.add_clip_rect()) or [`tm_draw2d_api->add_sub_clip_rect()`]({{docs}}plugins/ui/draw2d.h.html#structtm_draw2d_api.add_sub_clip_rect()). This gives you a clipping ID that can be passed as part of the Draw or UI style.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Responder scopes | *Responder Scopes* are used to control which controls can respond to keyboard input. Typically, when a control is *Active*, it, and all its parent controls can respond to keyboard input. For example, if the control is inside a scrollview, the scrollview will respond to scroll keypresses, while the tab that hosts the scrollview may respond to commands such as Ctrl+F.<br><br>Being an immediate GUI system, *The Machinery* doesn’t have an explicit concept of “child” and “parent” controls. Instead we use the concept of *Responder Scopes*. A parent control first calls [`begin_responder_scope()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.begin_responder_scope()), then draws all its child controls and finally calls [`end_responder_scope()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.end_responder_scope()). This establishes a parent-child relationship for the purpose of keyboard interaction.<br><br>When a control becomes *Active*, the current set of Responder Scopes is saved as the *Responder Chain*. This is the list of controls that can respond to a keyboard action. To test if your control should act on keyboard input, you can call [`in_responder_chain()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.in_responder_chain()).<br><br>Note: We currently don’t have any mechanism to check if other controls in the Responder Chain have “consumed” keyboard input, so if you have multiple controls in the same chain that respond to the same keyboard command, you may run into trouble.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

Bellow, we have a higher-level view of the steps needed to implement our interaction logic:


1. Create a id with [`tm_ui_api→make_id()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.make_id());
2. Check if the button is already active with [`tm_ui_api→is_active()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.is_active()), it will return a pointer for a 16Kb buffer that you can use to keep custom data needed while the button is active;
3. Check if the mouse is hovering the button, and set activation `next_hover` variable according. At the end of the frame, the UI system will set hover to our control id case no other control changed next_hover after us;
4. Case the hover variable contains our control id and mouse is pressed, set it as the active one, which is done which [`tm_ui_api→set_active()`]({{docs}}plugins/render_graph/render_graph.h.html#structtm_render_graph_setup_api.set_active()), a pointer to the 16Kb buffer will be returned so you can cast it to control custom data, note that we need to pass a hash to the function identifying this data;
5. Case our button is active and mouse was released, the control is considered clicked, and we call [`tm_ui_api→clear_active()`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api.clear_active()) to deactivate him;
6. Now we can check if the mouse is hovering our control and use either the active or hovering color depending on we are the active control or not;

With this in mind, the complete code will be the following:


- ui_custom_controls.h:

```C
    ...
    typedef struct tm_ui_circular_button_data_t {
        const char *name;
        uint32_t frames_active;
    } tm_ui_circular_button_data_t;
    
    typedef struct tm_ui_circular_button_t
    {
        uint64_t id;
    
        tm_vec2_t center;
        float radius;
        tm_color_srgb_t background_color;
        tm_color_srgb_t hover_color;
        tm_color_srgb_t clicked_color;
    
        const char *text;
        const struct tm_color_srgb_t text_color;
    } tm_ui_circular_button_t;
    ...
```

- ui_custom_controls.c:

```C
    ...
    
    bool circular_button(struct tm_ui_o *ui, const struct tm_ui_style_t *uistyle, const tm_ui_circular_button_t *c)
    {
        // Step 1
        // tm_ui_buffer_t contains information needed when creating a custom control
        tm_ui_buffers_t uib = tm_ui_api->buffers(ui);
        const uint64_t id = c->id ? c->id : tm_ui_api->make_id(ui);
        
        // Step 2
        // is_active will return a pointer for user defined data up to 16KB
        tm_ui_circular_button_data_t *active = (tm_ui_circular_button_data_t *)tm_ui_api->is_active(ui, id, TM_UI_ACTIVE_DATA__CIRCULAR_BUTTON);
        if (active) {
            TM_LOG("active data -> name: %s, frames_active: %u\n", active->name, active->frames_active);
            active->frames_active++;
        }
    
        // convert tm_ui_style_t to tm_draw2d_style_t
        tm_draw2d_style_t style;
        tm_ui_api->to_draw_style(ui, &style, uistyle);
        style.color = c->background_color;
        
        // Step 3
        bool clicked = false;
        bool inside = tm_vec2_in_circle(uib.input->mouse_pos, c->center, c->radius);
        if (inside)
            uib.activation->next_hover = id;
        
        // Step 4
        if (uib.activation->hover == id && uib.input->left_mouse_pressed) {
            active = tm_ui_api->set_active(ui, id, TM_UI_ACTIVE_DATA__CIRCULAR_BUTTON);
            if (active)
                *active = (tm_ui_circular_button_data_t){ .name = "circular_button", .frames_active = 0 };
            tm_ui_api->set_responder_chain(ui, 0);
        }
        
        // Step 5
        if (active && uib.input->left_mouse_released) {
            clicked = inside;
            tm_ui_api->clear_active(ui);
        }
        
        // Step 6
        if (inside) {
            if (active)
                style.color = c->clicked_color;
            else if (uib.activation->hover == id)
                style.color = c->hover_color;
        }
    
        tm_ui_api->reserve_draw_memory(ui);
        tm_draw2d_api->fill_circle(uib.vbuffer, uib.ibuffers[uistyle->buffer], &style, c->center, c->radius);
    
        return clicked;
    }
    
    ...
```

## Drawing text

The last thing we need is to draw some text inside our button. You'll need to call [`tm_draw2d_api→draw_glyphs()`]({{docs}}plugins/ui/draw2d.h.html#structtm_draw2d_api.draw_glyphs()) to fill UI buffers with text information. It takes as one of its arguments an array of glyphs indices that point to the corresponding [`tm_font_glyph_t`]({{docs}}plugins/ui/draw2d.h.html#structtm_font_glyph_t) glyph inside the [`tm_font_t`]({{docs}}plugins/ui/draw2d.h.html#structtm_font_t) structure. To get this information, we first need to convert the desired text to an array of codepoints using [`tm_unicode_api→utf8_decode_n()`]({{docs}}foundation/unicode.h.html#structtm_unicode_api.utf8_decode_n()) and pass them to [`tm_font_api→glyphs()`]({{docs}}plugins/ui/draw2d.h.html#structtm_font_api.glyphs()) . Thus, add the following lines to the source code:

With this in mind, the complete code will be the following:


- ui_custom_controls.h:

```C
    ...
    
    typedef struct tm_ui_circular_button_t
    {
       ...
        uint32_t icon;
        const char *text;
        const struct tm_color_srgb_t text_color;
    } tm_ui_circular_button_t;
    ...
```


- ui_custom_controls.c:

```C
    ...
    
    bool circular_button(struct tm_ui_o *ui, const struct tm_ui_style_t *uistyle, const tm_ui_circular_button_t *c)
    {
        ...
        // Inscribe a quad in button circle
        const float side = c->radius * sqrtf(2);
        tm_rect_t text_rect = tm_rect_center_dim(c->center, (tm_vec2_t){ side, side });
    
        tm_ui_api->reserve_draw_memory(ui);
        style.clip = tm_draw2d_api->add_sub_clip_rect(uib.vbuffer, style.clip, text_rect);
    
        // Get glyphs from our text
        uint16_t glyphs[128];
        uint32_t n = 0;
        {
            uint32_t codepoints[128];
            n = tm_unicode_api->utf8_decode_n(codepoints, 128, tm_or(c->text, ""));
            tm_font_api->glyphs(style.font->info, glyphs, codepoints, 128);
        }
        tm_vec2_t text_pos = {
            .x = c->center.x - side / 2.f,
            .y = middle_baseline(text_rect.y, text_rect.h, style.font->info, 1.f),
        };
        style.color = c->text_color;
        tm_draw2d_api->draw_glyphs(uib.vbuffer, uib.ibuffers[uistyle->buffer], &style, text_pos, glyphs, n);
    
        return clicked;
    }
    
    ...
```


We now have a custom button implementation that can be used across your projects. Please extend it and show us your results.

