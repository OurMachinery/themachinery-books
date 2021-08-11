
# Profiler Tab

The profiler tab will display all scopes that have been added to the profiler API. With the tab, you can record for a few moments all scopes and then afterward analyze them.

![](https://paper-attachments.dropbox.com/s_5086E710AFB88B222C81207791AF7092731DB9D2900AFABEA044A0AC0B80DFFB_1625602954215_image.png)

You can use the profiler API defined in the [foundation/profiler]({{docs}}foundation/profiler.h.html#profiler.h).h. in your own projects.
After you have loaded the [`tm_profiler_api`]({{docs}}foundation/profiler.h.html#structtm_profiler_api) in your plugin load function.

| Profiler Macros                                              |
| ------------------------------------------------------------ |
| **[TM_PROFILER_BEGIN_FUNC_SCOPE()]({{docs}}foundation/profiler.h.html#tm_profiler_begin_func_scope()) / [TM_PROFILER_END_FUNC_SCOPE()]({{docs}}foundation/profiler.h.html#tm_profiler_end_func_scope())** |
| Starts a profiling scope for the current function. The scope in the profiler will have this name. |
| **[TM_PROFILER_BEGIN_LOCAL_SCOPE(tag)]({{docs}}foundation/profiler.h.html#tm_profiler_begin_local_scope()) / [TM_PROFILER_END_LOCAL_SCOPE(tag)]({{docs}}foundation/profiler.h.html#tm_profiler_end_local_scope())** |
| The call to this macro starts a local profiler scope. The scope is tagged with the naked word tag (it gets stringified by the macro). Use a local profiler scope if you need to profile parts of a function. |

*Example:*

```c
void my_function({{base_url}}*some arguments*/){
   TM_PROFILER_BEGIN_FUNC_SCOPE()
   // .. some code
   TM_PROFILER_END_FUNC_SCOPE()
}
```
