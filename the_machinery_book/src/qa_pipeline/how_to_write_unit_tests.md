This walkthrough introduces you to unit-tests.exe and shows you how to use it with The Machinery. You will learn about:

- How to run tests
- How to constantly monitor your changes
- How to write tests in your plugin

This walkthrough expects basic knowledge on how to create a plugin and how a plugin is structured. If you are missing this knowledge, then you can find out more [here]({{base_url}}/the_machinery_book/extending_the_machinery/the_plugin_system.html).

> **Note:** At this point, the testing framework is in the beginning stage. We are extending its capabilities overtime to meet the needs of modern game development QA pipelines.


## **About unit-tests**

You can find the executable alongside `tmbuild` or the machinery executable in the `bin/ folder.` If you wanted to make the unit-tests executable globally accessible, you need to add it to your path environment variable. As you may have noticed, ensuring the quality of your build, `tmbuild` will run all unit tests of all plugins at the end of its build process. When you add a unit test to your plugin, it is guaranteed that its unit tests run every time you build. This is, of course, only guaranteed if the plugin system can find the plugin and its test.

> **Note:** unit-tests will assume that the plugins live in a folder relative to the executable in the standardized folder plugins. If you need to load a plugin that is not in this folder, you need to provide a valid path via `-p/--plugin` so that unit-tests can find and run your tests.


## **How to run tests**

To run all unit tests, execute unit-test, and it will run all tests besides the slow execution path tests. To run all unit tests, including the *"slow"* ones, you run `unit-tests.exe -s/--slow-paths`

> **Note:** You may have noticed that if you run `tmbuild` regularly, you are lucky and win in the "lottery" from time to time. This means `tmbuild` will run all unit tests also the slow ones via `unit-tests`.


## **How to constantly monitor your changes**

Like the editor, `unit-tests` supports [hot reloading](https://ourmachinery.com/post/dll-hot-reloading-in-theory-and-practice/). In a nutshell, whenever plugins are rebuilt `unit-tests` can detect this and rerun the tests. To run in hot-reload mode start`unit-tests` with the `-r/--hot-reload` argument.

*When could this be useful?*
It can be helpful on CI Server where build and test servers are different. The build server's final build step uploads the generated `dlls` to the test server if everything works fine. The test server is monitoring the filesystem, and whenever the dlls change, `unit-tests` would rerun all tests, also the slow ones, to ensure that all works. It could save time on the build server so the build times are faster and the developer knows quicker if the build fails. Also, the build server does not need a graphics card to run eventual graphic pipeline-related tests. The test server, on the other hand, could run such tests.



## **How to write your tests**

All that is needed is to write tests is to register them via the [TM_UNIT_TEST_INTERFACE_NAME](http://#). You can find the interface in the [unit_tests.h](http://#). [TM_UNIT_TEST_INTERFACE_NAME](http://#) expects a pointer of the type [tm_unit_test_i](http://#). This interface expects a name and a function pointer to the test entry function.


```c
// Interface for running unit tests. To find all unit test, query the API registry for
// `TM_UNIT_TEST_INTERFACE_NAME` implementations.
typedef struct tm_unit_test_i
{
    // Name of this unit test.
    const char *name;

    // Runs unit tests, using the specified test runner. The supplied allocator can be used for
    // any allocations that the unit test needs to make.
    void (*test)(tm_unit_test_runner_i *tr, struct tm_allocator_i *a);
} tm_unit_test_i;
```

At this point, we have not tackled the following possible questions:

- Where and how do we register the interface?
- How could this interface look like?
- How does a test itself look like?

**Let us walk through those questions:**

*Where and how do we register the interface?*
We need to register our tests in the same function as everything else that needs to be executed when a plugin loads: in our `tm_load_plugin`. It may look like this:


```c
#include <foundation/unit_test.h>
//...
// my amazing plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;
    //...
    tm_add_or_remove_implementation(reg, load, TM_UNIT_TEST_INTERFACE_NAME, my_unit_tests);
}
```

Here we register our test interface to the `TM_UNIT_TEST_INTERFACE_NAME`.

*How could this interface look like?*
After we have done this, all we need to do is declarer our `my_unit_tests`. It is as easy as it gets:

```c
#include <foundation/unit_test.h>
//...
tm_unit_test_i *entity_unit_test = &(tm_unit_test_i){
    .name = "my_unit_tests",
    .test = test_function,
};
```

*How does a test itself look like?*
All that's left is to write the test. Let us write this test. In its core all we need to do is write a function of the signature: `(tm_unit_test_runner_i *tr, struct tm_allocator_i *a)`. In its body, we can define our tests.


```c
static void test_function(tm_unit_test_runner_i *test_runner, tm_allocator_i *allocator)
{
    //.. code
}
```

The test runner variable test_runner is needed to communicate back to the test suite about failures etc. The following [macros](https://ourmachinery.com//apidoc/foundation/unit_test.h.html#tm_unit_test()) will help you write tests. They are the heart of the actual tests.

| **Macro**       | **Arguments**                         | **Description**                                              |
| --------------- | ------------------------------------- | ------------------------------------------------------------ |
| TM_UNIT_TEST    | (test_runner, assertion)              | Unit test macro. Tests the `assertion` using the test runner `test_runner`. |
| TM_UNIT_TESTF   | (test_runner, assertion, format, ...) | As `TM_UNIT_TEST()` but records a formatted string in case of error. |
| TM_EXPECT_ERROR | (test_runner, error)                  | Expect the error message `error`. If the error message doesn't appear before the next call to `record()`, or if another error message appears before it, this will be considered a unit test failure.<br><br>Note that for `TM_EXPECT_ERROR` to work properly, you must redirect error messages to go through the test runner, so that it can check that the error message matches what's expected. |

It's time for some tests. Let us write some tests for [carrays](https://ourmachinery.com//apidoc/foundation/carray.inl.html#carray.inl)

```c
#include <foundation/unit_test.h>
#include <foundation/carray.inl>
//.. other code
static void test_function(tm_unit_test_runner_i *test_runner, tm_allocator_i *allocator)
{
    /*carray*/ int32_t *a = 0;
    TM_UNIT_TEST(test_runner, tm_carray_size(a) == 0);
    TM_UNIT_TEST(test_runner, tm_carray_capacity(a) == 0);
    TM_UNIT_TEST(test_runner, a == 0);
    tm_carray_push(a, 1, &allocator);

    TM_UNIT_TEST(test_runner, tm_carray_size(a) == 1);
    TM_UNIT_TEST(test_runner, tm_carray_capacity(a) == 16);
    TM_UNIT_TEST(test_runner, a);
    TM_UNIT_TEST(test_runner, a[0] == 1);

    tm_carray_header(a)->size--;

    TM_UNIT_TEST(test_runner, tm_carray_size(a) == 0);
    TM_UNIT_TEST(test_runner, tm_carray_capacity(a) == 16);

    tm_carray_grow(a, 20, &allocator);
    tm_carray_header(a)->size = 20;

    TM_UNIT_TEST(test_runner, tm_carray_size(a) == 20);
    TM_UNIT_TEST(test_runner, tm_carray_capacity(a) == 32);
}
```

All that's left is to build via ``tmbuild`` our plugin and watch the console output if our tests fail. This is how you integrate your tests into the whole build pipeline. 

