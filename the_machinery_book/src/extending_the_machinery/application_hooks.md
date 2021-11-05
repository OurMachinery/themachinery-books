# Application Hook's

The Machinery allows you to hook your code into specific customization points. Those points happen in different phases and have specific purposes. The biggest difference between the Runner and the Editor is that only the customization points differ in the central update loop.

**Table of Content**

* auto-gen TOC;
{:toc}


## Application Create

![](https://www.dropbox.com/s/vsl0d53ty9rsvbi/tm_guide_app_hook_create.png?dl=1)
## Update

**Important side note** here `tm_plugin_tick_i` should **not** be used for **gameplay**. To manage your gameplay you should relay on the given gameplay hooks:

- Entity Component Systems
- Entity Component Engines
- Simulation Entry

They are the only recommended way of handling gameplay in the Engine.

>  **Note:** Plugin reloads only happen if a plugin has been identified as replaced.

### Editor

![](https://www.dropbox.com/s/ibyjx33p4lci62w/tm_guide_app_hooks_update_editor.png?dl=1)

### Runner

![](https://www.dropbox.com/s/9nq4ysh2gefzks1/tm_guide_app_hooks_update_runner.png?dl=1)

## Project Hooks

![](https://www.dropbox.com/s/jtsk5df9rykp8di/tm_guide_app_hook_project.png?dl=1)

## Application Shutdown

![](https://www.dropbox.com/s/ecssnn4hvv42avi/tm_guide_app_hook_shutdown.png?dl=1)

## Overview

| Interface                                                    | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)` | Entry point for all plugins                                  |
| `tm_plugin_init_i`                                           | Is typically called as early as possible after all plugins have been loaded. **Is not called when a plugin is reloaded.** |
| `tm_plugin_set_the_truth_i`                                  | Is called whenever the "main" Truth of the application changes. The "main" Truth is the primary Truth used for editing data in the application. **Under API Review** |
| `tm_render_pipeline_vt`                                      |                                                              |
| `tm_the_machinery_project_loaded_i`                          | Is called when ever a project is loaded.                     |
| `tm_plugin_reload_i`                                         | Is called whenever plugins are reloaded after the reload finishes. |
| `tm_plugin_tick_i`                                           | Is typically called as early as possible in the application main loop "tick". |
| A tab that is registered to `tm_tab_vt` and has a `tm_tab_vt.ui()` or `tm_tab_vt.hidden_update()` function. | Interface name for the tab `vtable`. Any part of the UI that can act as a tab should implement  this interface. |
| `tm_entity_register_engines_simulation_i_version` Is called at the beginning of a simulation (start up phase) and all Systems / Engines are registered to the entity context. `tm_entity_system_i.update()` or `tm_engine_i.update()` | Used to register a `tm_entity_register_engines_i` that should run in simulation mode with. More information in the designated chapter. [Entity Component System]({{the_machinery_book}}gameplay_coding/ecs/index.html) |
| `tm_entity_register_engines_editor_i_version`                | Used to register a `tm_entity_register_engines_i` that should run in editor mode with. |
| `tm_simulation_entry_i` `tm_simulation_entry_i.start()  ` `tm_simulation_entry_i.tick()` `tm_simulation_entry_i.stop()` | The Simulation Entry interface `tm_simulation_entry_i` makes it possible to choose a point of entry  for code that should run while the simulation (simulation tab or runner) is active.  More information in the designated chapter. [Simulation Entry]({{the_machinery_book}}/gameplay_coding/simulation_entry.html) |
| `tm_the_machinery_project_unloaded_i`                        | Is called when ever a project is unloaded.                   |
| `tm_the_machinery_project_saved_i`                           | Is called when ever a project is saved.                      |
| `tm_plugin_shutdown_i`                                       | Is called when the application shutdowns on all plugins that have a interface registered. **Is not called when a plugin is reloaded.** |