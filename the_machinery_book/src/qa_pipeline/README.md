# QA Pipeline

The Machinery comes with some built-in tools to support you in building games.

- [Unit Test Framework]({{docs}}foundation/unit_test.h.html#unit_test.h)
- [Integration Test Framework]({{docs}}foundation/integration_test.h.html#integration_test.h)
- [Profiler and profiling framework]({{docs}}foundation/profiler.h.html#profiler.h)
- [Memory leak Detection]({{docs}}foundation/memory_tracker.h.html#memory_tracker.h)

**Table of Content**

* auto-gen TOC;
{:toc}



## Profiler Tab

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
void my_function({{base_url}}/the_machinery_book/*some arguments*/){
   TM_PROFILER_BEGIN_FUNC_SCOPE()
   // .. some code
   TM_PROFILER_END_FUNC_SCOPE()
}
```

## Memory Usage Tab

The memory tab will display all memory consumed via any allocator. Temporary allocators will be listed as well. Besides the memory from the CPU allocators, you can also inspect device memory used and the memory consumed by your assets.

![](https://paper-attachments.dropbox.com/s_5086E710AFB88B222C81207791AF7092731DB9D2900AFABEA044A0AC0B80DFFB_1625603084539_image.png)



## Statistic Tab

Allows you to visualize different statistics from different sources. 

![](https://paper-attachments.dropbox.com/s_5086E710AFB88B222C81207791AF7092731DB9D2900AFABEA044A0AC0B80DFFB_1625603204224_image.png)


The Statistic tab consists of a Property View in which you can define your desired method of display and source. You can choose between Table, Line, or no visualization method. As sources, the engine will offer you any of the profiler scopes.

![](https://paper-attachments.dropbox.com/s_5086E710AFB88B222C81207791AF7092731DB9D2900AFABEA044A0AC0B80DFFB_1625604230068_image.png)

