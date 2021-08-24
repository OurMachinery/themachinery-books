# Application Hook's

The Machinery allows you to hook your code into specific customization points. Those points happen in different phases and have specific purposes. The biggest difference between the Runner and the Editor is that only the customization points differ in the central update loop.

**Table of Content**

* auto-gen TOC;
{:toc}


## Application Create

![](https://www.dropbox.com/s/vsl0d53ty9rsvbi/tm_guide_app_hook_create.png?dl=1)
## Update

**Important side note** here `TM_PLUGIN_TICK_INTERFACE_NAME` should **not** be used for **gameplay**. To manage your gameplay you should relay on the given gameplay hooks:

- Entity Component Systems
- Entity Component Engines
- Simulate Entry

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
| `TM_PLUGIN_INIT_INTERFACE_NAME`                              | Is typically called as early as possible after all plugins have been loaded. **Is not called when a plugin is reloaded.** |
| `TM_PLUGIN_SET_THE_TRUTH_INTERFACE_NAME`                     | Is called whenever the "main" Truth of the application changes. The "main" Truth is the primary Truth used for editing data in the application. **Under API Review** |
| `TM_RENDER_PIPELINE_INTERFACE_NAME`                          |                                                              |
| `TM_THE_MACHINERY_PROJECT_LOADED_INTERFACE_NAME`             | Is called when ever a project is loaded.                     |
| `TM_PLUGIN_RELOAD_INTERFACE_NAME`                            | Is called whenever plugins are reloaded after the reload finishes. |
| `TM_PLUGIN_TICK_INTERFACE_NAME`                              | Is typically called as early as possible in the application main loop "tick". |
| A tab that is registered to `TM_TAB_VT_INTERFACE_NAME` and has a `tm_tab_vt.ui()` or `tm_tab_vt.hidden_update()` function. | Interface name for the tab `vtable`. Any part of the UI that can act as a tab should implement  this interface. |
| `TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME` Is called at the beginning of a simulation (start up phase) and all Systems / Engines are registered to the entity context. `tm_entity_system_i.update()` or `tm_engine_i.update()` | Used to register a `tm_entity_register_engines_i` that should run in simulation mode with. More information in the designated chapter. [Entity Component System]({{the_machinery_book}}gameplay_coding/ecs/index.html) |
| `TM_ENTITY_EDITOR_REGISTER_ENGINES_INTERFACE_NAME`           | Used to register a `tm_entity_register_engines_i` that should run in editor mode with. |
| `TM_SIMULATE_ENTRY_INTERFACE_NAME` `tm_simulate_entry_i.start()  ` `tm_simulate_entry_i.tick()` `tm_simulate_entry_i.stop()` | The Simulate Entry interface `tm_simulate_entry_i` makes it possible to choose a point of entry  for code that should run while the simulation (simulation tab or runner) is active.  More information in the designated chapter. [Simulate Entry]({{the_machinery_book}}/gameplay_coding/simulate_entry.html) |
| `TM_THE_MACHINERY_PROJECT_UNLOADED_INTERFACE_NAME`           | Is called when ever a project is unloaded.                   |
| `TM_THE_MACHINERY_PROJECT_SAVED_INTERFACE_NAME`              | Is called when ever a project is saved.                      |
| `TM_PLUGIN_SHUTDOWN_INTERFACE_NAME`                          | Is called when the application shutdowns on all plugins that have a interface registered. **Is not called when a plugin is reloaded.** |