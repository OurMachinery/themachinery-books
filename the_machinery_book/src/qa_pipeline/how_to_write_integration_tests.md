# How to write integration tests

This walkthrough shows you how to write integration tests with our integration test framework. You will learn about:

- How an integration test differs from a unit test.
- Where to find the integration test framework and how to write a test
- How to run an integration test.

## **About integration tests**

Integration testing is the phase in testing software in which individual software modules are combined and tested as a group. Integration testing is conducted to evaluate a system's compliance or its interaction as a whole within specified functional requirements. 
Its generally used after unit testing to ensure that the composition of the software works. It is a potent tool to validate certain bugs that are hard to reproduce only after using software extensively. You can simulate this with integration tests. Besides, it is a very powerful tool validating that a bug fix was successful.

By their very nature, integration tests are slower and more fragile than unit tests, but they can also find issues that are hard to detect with regular unit tests. Each integration test runs in a specific "context", identified by a string hash. The context specifies the "scaffolding" is set up before the unit test runs.

## **How to write integration tests**

**Where to find the integration test framework?**

The integration test framework can be found in the [integration_test.h](https://ourmachinery.com//apidoc/foundation/integration_test.h.html) ,and is part of the foundation library. We need to include this header file, and then we can start writing our tests.


    #include <foundation/integration_test.h>

To write a test you need to register it via the [TM_INTEGRATION_TEST_INTERFACE_NAME](https://ourmachinery.com//apidoc/foundation/integration_test.h.html#tm_integration_test_interface_name). It expects a pointer of the type [tm_integration_test_i](https://ourmachinery.com//apidoc/foundation/integration_test.h.html#structtm_integration_test_i). This interface expects a name and a function pointer to the test function (tick). Also, it expects a context. The context is a string hash. For example: `TM_INTEGRATION_TEST_CONTEXT__THE_MACHINERY_EDITOR`.


```c
// Interface for integration tests.
typedef struct tm_integration_test_i
{
    // Name of the test.
    const char *name;
    // Context that this test will run in. Tests will only be run in contexts that match their
    // `context` setting.
    tm_strhash_t context;
    // Ticks the test. The `tick()` function will be called repeatedly until all it's `wait()` calls
    // have completed.
    void (*tick)(tm_integration_test_runner_i *);
} tm_integration_test_i;
```

At this point, we have not tackled the following possible questions:

- Where and how do we register the interface?
- How could this interface look like?
- How does a test itself look like?

**Let us walk those questions through:**

*Where and how do we register the interface?*

We need to register our tests in the same function as everything else that needs to be executed when a plugin loads: in our `tm_load_plugin`.


```c
// my amazing plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;
    //...
    tm_add_or_remove_implementation(reg, load, TM_INTEGRATION_TEST_INTERFACE_NAME, my_integration_tests);
}
```

Here we register our test interface to the `TM_INTEGRATION_TEST_INTERFACE_NAME`.

*How could this interface look like?*

After we have done this, we need to declare our `my_integration_tests.` 


```c
tm_integration_test_i my_integration_tests = {
    .name = "stress-test",
    //Context that specifies a running The Machinery editor application
    .context = TM_INTEGRATION_TEST_CONTEXT__THE_MACHINERY_EDITOR,
    .tick = my_test_tick,
};
```

The name field is important because, later on, we need to use this name when we want to run the test. The context makes sure that it runs and boots up the Editor. `TM_INTEGRATION_TEST_CONTEXT__THE_MACHINERY_EDITOR` is defined in `#include <foundation/integration_test.h>`. The function `my_test_tick` gets called and the magic can happen.

*How does a test itself look like?*

 Let us write this test. We need to write a function of the signature: `(tm_integration_test_runner_i *)`.  In its body, we can define our tests.


```c
static void my_test_tick(tm_integration_test_runner_i *test_runner)
{
  //.. code
}
```

The test runner variable `test_runner` is needed to communicate back to the test suite about failures etc.  The following [macros](https://ourmachinery.com//apidoc/foundation/integration_test.h.html) will help you write tests. They are the heart of the tests.

| **Macro**    | **Arguments**          | **Description**                                              |
| ------------ | ---------------------- | ------------------------------------------------------------ |
| TM_WAIT      | test_runner, second    | Waits for the specified time inside an integration test.     |
| TM_WAIT_LOOP | test_runner, second, i | Since `TM_WAIT()` uses the `__LINE__` macro to uniquely identify wait points, it doesn't work when called in a loop. In this case you can use `TM_WAIT_LOOP()` instead. It takes an iteration parameter `i` that uniquely identifies this iteration of the loop (typically it would just be the iteration index). This together with `__LINE__` gives a unique identifier for the wait point. |

> **`TM_WAIT_LOOP` WARNING**
>
> If you have multiple nested loops, be aware that using just the inner loop index j is not enough to uniquely identify the wait point since it is repeated for each outer loop iteration. Instead, you want to combine the outer and inner indexes.

Lets write some example:

```c
#include <foundation/integration_test.h>
static void my_test_tick(tm_integration_test_runner_i *test_runner)
{
    const float step_time = 0.5f;
    if (TM_WAIT(tr, step_time))
    open(tr, "C:\\work\\sample-projects\\modular-dungeon-kit\\project.the_machinery_dir");
    if (TM_WAIT(tr, step_time))
    save_to_asset_database(tr, "C:\\work\\sample-projects\\modular-dungeon-kit\\modular-dungeon-kit.the_machinery_db");
    // ...
}
```


## **How do we run an integration test?**

To run your newly created integration test, we need to build the project via tmbuild. Then start The Machinery with the `-t/--test [NAME]` parameter. It runs the specified integration test. 


> You can use multiple --test arguments to run multiple tests. This will boot up the engine and run your integration tests.

*Example:*

    ./bin/the-machinery.exe --test stress-test

