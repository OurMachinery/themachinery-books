## Premake Guide

At Our Machinery we are using [Premake](https://premake.github.io/) for our meta build system generator. Premake generates for us the actual build scripts that we then build with `tmbuild` our one-click build tool. More on tmbuild [here](./tmbuild.html).

**Table of Content**

* {:toc}

## Why Use a Build Configurator?

Maintaining different *Makefiles* and *Visual Studio Solution* files for a cross platform project can be a lot of work. Especially since you have to adjust the generator a lot for every new platform you support.

- Writing [Makefiles](https://www.cs.swarthmore.edu/~newhall/unixhelp/howto_makefiles.html) even for the simplest projects can be a tedious effort without automation, and it is difficult to debug.
- Visual Studio Solution and Project Files are pre-generated, but are not designed to be easy to edit by hand, so resolving merge conflicts with them can be frustrating.

Several build tools exist that allow us to avoid these issues. [CMake](https://cmake.org/) is widely used, but tends to have a high learning curve and its scripting language is not the easiest to learn. Moreover it can very hard to debug.

> **Source:** This information is based on [Getting Started With Premake by Johannes Peter](http://blog.johannesmp.com/2016/10/29/getting-started-with-premake/)

## What is premake

 [Premake5](https://premake.github.io/) is a Lightweight, Open-source, Lua-based alternative to CMake. As with CMake, Premake allows you to define the structure and contents of your project and then dynamically generate whatever build files (Makefiles, VS Solutions, Xcode Projects, etc) you need at the time.

At the core of Premake5 is a **premake5.lua** file that describes your project (what programming language it uses, where to find source files, what dependencies it has, etc.). ‘**premake5.lua**’ is to ***Premake*** what is ‘**Makefile**’ is to *[GNU Make](https://www.gnu.org/software/make/)* or a project/sln file to Visual Studios.

Because *premake5.lua* allows you to uniquely generate whatever build files you need in seconds, you no longer need to version them in your repository. You configure your version control to [ignore](https://git-scm.com/docs/gitignore) the build files, and version the premake5.lua file instead. Resolving merge conflicts on a premake5.lua file is far more sane than on a Visual Studio project file.

Once you have a premake5.lua file, you can run the premake executable to generate your desired project files. For example:

- To generate a Makefile on Linux you run `./premake5 vs20122`
- To generate a VS 2022 Solution on Windows you run `premake5 vs2022`

> **Source:** This information is based on [Getting Started With Premake by Johannes Peter](http://blog.johannesmp.com/2016/10/29/getting-started-with-premake/)

## The Basic The Machinery Premake Setup

Since Premake is lua based you can make use of Lua's features. In this case we show a simple premake file for a plugin:

```lua
-- premake5.lua
-- version: premake-5.0.0-alpha14

function snake_case(name)
    return string.gsub(name, "-", "_")
end

-- Include all project files from specified folder
function folder(t)
    if type(t) ~= "table" then t = {t} end
    for _,f in ipairs(t) do
        files {f .. "/**.h",  f .. "/**.c", f .. "/**.inl", f .. "/**.cpp", f .. "/**.m", f .. "/**.tmsl"}
    end
end

function check_env(env)
    local env_var = os.getenv(env)

    if env_var == nil then
        return false
    end
    return true
end

function tm_lib_dir(path)
    local lib_dir = os.getenv("TM_LIB_DIR")

    if not check_env("TM_LIB_DIR") then
        error("TM_LIB_DIR not set")
        return nil
    end

    return lib_dir .. "/" .. path
end

oldlibdirs = libdirs
function libdirs(path)
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    sdk_dir = os.getenv("TM_SDK_DIR")
    oldlibdirs { 
        sdk_dir .. "/lib/" .. _ACTION .. "/%{cfg.buildcfg}",
        sdk_dir .. "/bin/%{cfg.buildcfg}",
        dirs
    }
    oldlibdirs { 
        sdk_dir .. "/lib/" .. _ACTION .. "/%{cfg.buildcfg}",
        sdk_dir .. "/bin/%{cfg.buildcfg}",
        dirs
    }
end

-- Make incluedirs() also call sysincludedirs()
oldincludedirs = includedirs
function includedirs(dirs)
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    sdk_dir = os.getenv("TM_SDK_DIR")
    oldincludedirs { 
        sdk_dir .. "/headers",
        sdk_dir ,
         dirs
    }
    sysincludedirs { 
        sdk_dir .. "/headers",
        sdk_dir ,
        dirs
    }
end
-- Makes sure the debugger points to the machinery
function set_debugger_to_engine()
    local sdk_dir = os.getenv("TM_SDK_DIR")
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    local debug_path_source = ""
    local debug_path_binary = ""
    if os.target() == "windows" then
         debug_path_source = "/bin/Debug/the-machinery.exe"
         debug_path_binary = "/bin/the-machinery.exe"
    else
         debug_path_source = "/bin/Debug/the-machinery"
         debug_path_binary = "/bin/the-machinery"
    end
    if os.isfile(sdk_dir..""..debug_path_source) then
        debugcommand(sdk_dir..debug_path_source)
    elseif os.isfile(sdk_dir..""..debug_path_binary) then
        debugcommand(sdk_dir..debug_path_binary)
    else
        error("Could not find '"..sdk_dir..""..debug_path_binary.."' nor '"..sdk_dir..""..debug_path_source.."'\nSuggestion: Please make sure the TM_SDK_DIR enviroment variable is pointing to the correct folder.")
    end
end


newoption {
    trigger     = "clang",
    description = "Force use of CLANG for Windows builds"
}

workspace "test-plugin"
    configurations {"Debug", "Release"}
    language "C++"
    cppdialect "C++11"
    flags { "FatalWarnings", "MultiProcessorCompile" }
    warnings "Extra"
    inlining "Auto"
    sysincludedirs { "" }
    targetdir "bin/%{cfg.buildcfg}"

filter "system:windows"
    platforms { "Win64" }
    systemversion("latest")

filter {"system:linux"}
    platforms { "Linux" }

filter { "system:windows", "options:clang" }
    toolset("msc-clangcl")
    buildoptions {
        "-Wno-missing-field-initializers",   -- = {0} is OK.
        "-Wno-unused-parameter",             -- Useful for documentation purposes.
        "-Wno-unused-local-typedef",         -- We don't always use all typedefs.
        "-Wno-missing-braces",               -- = {0} is OK.
        "-Wno-microsoft-anon-tag",           -- Allow anonymous structs.
    }
    buildoptions {
        "-fms-extensions",                   -- Allow anonymous struct as C inheritance.
        "-mavx",                             -- AVX.
        "-mfma",                             -- FMA.
    }
    removeflags {"FatalLinkWarnings"}        -- clang linker doesn't understand /WX

filter "platforms:Win64"
    defines { "TM_OS_WINDOWS", "_CRT_SECURE_NO_WARNINGS" }
    includedirs { }
    staticruntime "On"
    architecture "x64"
    libdirs { }
    disablewarnings {
        "4057", -- Slightly different base types. Converting from type with volatile to without.
        "4100", -- Unused formal parameter. I think unusued parameters are good for documentation.
        "4152", -- Conversion from function pointer to void *. Should be ok.
        "4200", -- Zero-sized array. Valid C99.
        "4201", -- Nameless struct/union. Valid C11.
        "4204", -- Non-constant aggregate initializer. Valid C99.
        "4206", -- Translation unit is empty. Might be #ifdefed out.
        "4214", -- Bool bit-fields. Valid C99.
        "4221", -- Pointers to locals in initializers. Valid C99.
        "4702", -- Unreachable code. We sometimes want return after exit() because otherwise we get an error about no return value.
    }
    linkoptions {"/ignore:4099"}
    buildoptions {"/utf-8"}     

filter {"platforms:Linux"}
    defines { "TM_OS_LINUX", "TM_OS_POSIX" }
    includedirs { }
    architecture "x64"
    toolset "clang"
    buildoptions {
        "-fms-extensions",                   -- Allow anonymous struct as C inheritance.
        "-g",                                -- Debugging.
        "-mavx",                             -- AVX.
        "-mfma",                             -- FMA.
        "-fcommon",                          -- Allow tentative definitions
    }
    libdirs { }
    disablewarnings {
        "missing-field-initializers",   -- = {0} is OK.
        "unused-parameter",             -- Useful for documentation purposes.
        "unused-local-typedef",         -- We don't always use all typedefs.
        "missing-braces",               -- = {0} is OK.
        "microsoft-anon-tag",           -- Allow anonymous structs.
    }
    removeflags {"FatalWarnings"}

filter "configurations:Debug"
    defines { "TM_CONFIGURATION_DEBUG", "DEBUG" }
    symbols "On"
    filter "system:windows"
        set_debugger_to_engine() -- sets the debugger in VS Studio to point to the_machinery.exe

filter "configurations:Release"
    defines { "TM_CONFIGURATION_RELEASE" }
    optimize "On"

project "test-plugin"
    location "build/test-plugin"
    targetname "test-plugin"
    kind "SharedLib"
    language "C++"
    files {"*.inl", "*.h", "*.c"}
```

Wow this is a lot of code ... lets talk about the basics: `filter `, `workspace` and `project`

`filter {...}` allows you to set a filter for a specific configuiration or option.  For example:

```lua
filter "configurations:Debug"
    defines { "TM_CONFIGURATION_DEBUG", "DEBUG" }
    symbols "On"
    filter "system:windows"
        set_debugger_to_engine() -- sets the debugger in VS Studio to point to the_machinery.exe

filter "configurations:Release"
    defines { "TM_CONFIGURATION_RELEASE" }
    optimize "On"
```

This example tells Premake5 that on Debug we have the define `TM_CONFIGURATION_DEBUG` and we generate debug symbols : `symbols "On"` and only on windows we make sure that we point to the right debugger:

```lua
    filter "system:windows"
        set_debugger_to_engine() -- sets the debugger in VS Studio to point to the_machinery.exe
```

With this knowlege we still have not reduced the amount of code to think about! Yes that is right so lets just say: We can ignore 90% of the premake file and just take it as it is and only focus on the really important aspects:

```lua
--- more code we can ignore
workspace "test-plugin"
    configurations {"Debug", "Release"}
    language "C++"
    cppdialect "C++11"
    flags { "FatalWarnings", "MultiProcessorCompile" }
    warnings "Extra"
    inlining "Auto"
    sysincludedirs { "" }
    targetdir "bin/%{cfg.buildcfg}"
--- more code we can ignore
project "test-plugin"
    location "build/test-plugin"
    targetname "test-plugin"
    kind "SharedLib"
    language "C++"
    files {"*.inl", "*.h", "*.c"}
```

This defines our workspace. This woul be in VS our Solution:

```lua
workspace "test-plugin" --- The name of the Workspace == The Solution name in VS
    configurations {"Debug", "Release"} -- The configurations we offer
    language "C++" -- The Language in this case C++
    cppdialect "C++11" 
    flags { "FatalWarnings", "MultiProcessorCompile" } -- We treat warnings as errors and can compile with more cores
    warnings "Extra" -- That we basically show all warnings
    inlining "Auto"
    sysincludedirs { "" } -- making sure we have the system includes
    targetdir "bin/%{cfg.buildcfg}" -- where do we store our binary files, not our .d files etc...
```

The next important aspect is the project itself:

```lua
project "test-plugin" -- The name of the project in VS or the target in the Makefile
    location "build/test-plugin" -- Where do we want to store all our artifacts such as .d .obj etc
    targetname "test-plugin" -- The name of our executable, shared lib or static lib?
    kind "SharedLib" -- What kind? StaticLib, SharedLib, Executable?
    language "C++"-- What is our languge of implemntation? 
    files {"*.inl", "*.h", "*.c"} -- What files do we want to automagically include in our project?
```

If you want to add a new project to your premake file you can just add a new block such as the one above to to your premake file:

```lua
project "new-project" 
    location "build/new-project" 
    targetname "new-project" 
    kind "SharedLib" 
    language "C"
	cppdialect "C11" -- you can also add other things here!
    files {"*.inl", "*.h", "*.c"} 
```

This adds a new project called `new-project` to your premake file when you compile now the dll with the name ``new-project` will be build on Windows on Linux it will be a `.so` file.



## Advanced Premake5: Adding functions to make our live easier

The code example above is great but its quite a lot of work. This is something you can change. Since Premake5 is using Lua you can just write functions to bundle your code together. For example lets say we want a base for all our projects:

```lua
function base(name)
    project(name)
        language "C++"
        includedirs { "" }
end
```

And than we want to make sure that our plugins (.dlls) are all the same but easy to use:

```lua
function plugin(name)
    local sn = snake_case(name) -- function that converts a name to snake case
    base(name)
        location("build/plugins/" .. sn)
        kind "SharedLib"
        targetdir "bin/%{cfg.buildcfg}/plugins"
        targetname("tm_" .. sn)
        defines {"TM_LINKS_" .. string.upper(sn)}
        dependson("foundation")
        folder {"plugins/" .. sn}
        language "C++"
        includedirs { "" } -- A override (see above) that makes sure we have the right include dir also with the SDK dirs
end
```

This allows us to re-write our example from above:

```lua
plugin("test-plugin")
plugin("new-project")
```

Moreover we need a utility tool? No problem we can just write a function for this:

```lua
-- Project type for utility programs
function util(name)
    local sn = snake_case(name)
    base(name)
        location("build/" .. sn)
        kind "ConsoleApp"
        targetdir "bin/%{cfg.buildcfg}"
        defines { "TM_LINKS_FOUNDATION" }
        dependson { "foundation" }
        links { "foundation" }
        folder {"utils/" .. sn}
        filter { "platforms:Linux" }
            linkoptions {"-ldl", "-lanl", "-pthread"}
        filter {} -- clear filter for future calls
end
```

This allows for the following lines of code:

```lua
plugin("test-plugin")
plugin("new-project")
util("my-untility")
```



## The Machinery Project Recommendation

We recommend you to make use of one single premake file that manages all your plugins at one build. This avoids the need to go in each of the folder to build your project. As recommended in the the chapter [Project Setup: Possible folder structure for a project]({{base_url}}/getting_started/project_setup.html#possible-folder-structure-for-a-project) we recommend also to seperate your plugins into sub folders. The following image shows a potential setup for your game plugins:

![](https://www.dropbox.com/s/l1429g7p5xx8kj2/tm_guide_possible_subfolder.png?dl=1)

In here we have one single `premake` file and a single `libs.json` as well as the `libs` folder. This allows you to run `tmbuild` just in this folder and all plugins or the ones you want to build can be built at once. 

In this case the premake file could look like this:

> **TODO** move this to code snippets!

```lua
-- premake5.lua
-- version: premake-5.0.0-alpha14

function snake_case(name)
    return string.gsub(name, "-", "_")
end

-- Include all project files from specified folder
function folder(t)
    if type(t) ~= "table" then t = {t} end
    for _,f in ipairs(t) do
        files {f .. "/**.h",  f .. "/**.c", f .. "/**.inl", f .. "/**.cpp", f .. "/**.m", f .. "/**.tmsl"}
    end
end

function check_env(env)
    local env_var = os.getenv(env)

    if env_var == nil then
        return false
    end
    return true
end

function tm_lib_dir(path)
    local lib_dir = os.getenv("TM_LIB_DIR")

    if not check_env("TM_LIB_DIR") then
        error("TM_LIB_DIR not set")
        return nil
    end

    return lib_dir .. "/" .. path
end

oldlibdirs = libdirs
function libdirs(path)
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    sdk_dir = os.getenv("TM_SDK_DIR")
    oldlibdirs { 
        sdk_dir .. "/lib/" .. _ACTION .. "/%{cfg.buildcfg}",
        sdk_dir .. "/bin/%{cfg.buildcfg}",
        dirs
    }
    oldlibdirs { 
        sdk_dir .. "/lib/" .. _ACTION .. "/%{cfg.buildcfg}",
        sdk_dir .. "/bin/%{cfg.buildcfg}",
        dirs
    }
end

-- Make incluedirs() also call sysincludedirs()
oldincludedirs = includedirs
function includedirs(dirs)
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    sdk_dir = os.getenv("TM_SDK_DIR")
    oldincludedirs { 
        sdk_dir .. "/headers",
        sdk_dir ,
         dirs
    }
    sysincludedirs { 
        sdk_dir .. "/headers",
        sdk_dir ,
        dirs
    }
end
-- Makes sure the debugger points to the machinery
function set_debugger_to_engine()
    local sdk_dir = os.getenv("TM_SDK_DIR")
    if not check_env("TM_SDK_DIR") then
        error("TM_SDK_DIR not set")
        return
    end
    local debug_path_source = ""
    local debug_path_binary = ""
    if os.target() == "windows" then
         debug_path_source = "/bin/Debug/the-machinery.exe"
         debug_path_binary = "/bin/the-machinery.exe"
    else
         debug_path_source = "/bin/Debug/the-machinery"
         debug_path_binary = "/bin/the-machinery"
    end
    if os.isfile(sdk_dir..""..debug_path_source) then
        debugcommand(sdk_dir..debug_path_source)
    elseif os.isfile(sdk_dir..""..debug_path_binary) then
        debugcommand(sdk_dir..debug_path_binary)
    else
        error("Could not find '"..sdk_dir..""..debug_path_binary.."' nor '"..sdk_dir..""..debug_path_source.."'\nSuggestion: Please make sure the TM_SDK_DIR enviroment variable is pointing to the correct folder.")
    end
end


newoption {
    trigger     = "clang",
    description = "Force use of CLANG for Windows builds"
}

workspace "test-plugin"
    configurations {"Debug", "Release"}
    language "C++"
    cppdialect "C++11"
    flags { "FatalWarnings", "MultiProcessorCompile" }
    warnings "Extra"
    inlining "Auto"
    sysincludedirs { "" }
    targetdir "bin/%{cfg.buildcfg}"

filter "system:windows"
    platforms { "Win64" }
    systemversion("latest")

filter {"system:linux"}
    platforms { "Linux" }

filter { "system:windows", "options:clang" }
    toolset("msc-clangcl")
    buildoptions {
        "-Wno-missing-field-initializers",   -- = {0} is OK.
        "-Wno-unused-parameter",             -- Useful for documentation purposes.
        "-Wno-unused-local-typedef",         -- We don't always use all typedefs.
        "-Wno-missing-braces",               -- = {0} is OK.
        "-Wno-microsoft-anon-tag",           -- Allow anonymous structs.
    }
    buildoptions {
        "-fms-extensions",                   -- Allow anonymous struct as C inheritance.
        "-mavx",                             -- AVX.
        "-mfma",                             -- FMA.
    }
    removeflags {"FatalLinkWarnings"}        -- clang linker doesn't understand /WX

filter "platforms:Win64"
    defines { "TM_OS_WINDOWS", "_CRT_SECURE_NO_WARNINGS" }
    includedirs { }
    staticruntime "On"
    architecture "x64"
    libdirs { }
    disablewarnings {
        "4057", -- Slightly different base types. Converting from type with volatile to without.
        "4100", -- Unused formal parameter. I think unusued parameters are good for documentation.
        "4152", -- Conversion from function pointer to void *. Should be ok.
        "4200", -- Zero-sized array. Valid C99.
        "4201", -- Nameless struct/union. Valid C11.
        "4204", -- Non-constant aggregate initializer. Valid C99.
        "4206", -- Translation unit is empty. Might be #ifdefed out.
        "4214", -- Bool bit-fields. Valid C99.
        "4221", -- Pointers to locals in initializers. Valid C99.
        "4702", -- Unreachable code. We sometimes want return after exit() because otherwise we get an error about no return value.
    }
    linkoptions {"/ignore:4099"}
    buildoptions {"/utf-8"}     

filter {"platforms:Linux"}
    defines { "TM_OS_LINUX", "TM_OS_POSIX" }
    includedirs { }
    architecture "x64"
    toolset "clang"
    buildoptions {
        "-fms-extensions",                   -- Allow anonymous struct as C inheritance.
        "-g",                                -- Debugging.
        "-mavx",                             -- AVX.
        "-mfma",                             -- FMA.
        "-fcommon",                          -- Allow tentative definitions
    }
    libdirs { }
    disablewarnings {
        "missing-field-initializers",   -- = {0} is OK.
        "unused-parameter",             -- Useful for documentation purposes.
        "unused-local-typedef",         -- We don't always use all typedefs.
        "missing-braces",               -- = {0} is OK.
        "microsoft-anon-tag",           -- Allow anonymous structs.
    }
    removeflags {"FatalWarnings"}

filter "configurations:Debug"
    defines { "TM_CONFIGURATION_DEBUG", "DEBUG" }
    symbols "On"
    filter "system:windows"
        set_debugger_to_engine() -- sets the debugger in VS Studio to point to the_machinery.exe

filter "configurations:Release"
    defines { "TM_CONFIGURATION_RELEASE" }
    optimize "On"

function base(name)
    project(name)
        language "C++"
        includedirs { "" }
end

function plugin(name)
    local sn = snake_case(name) -- function that converts a name to snake case
    base(name)
        location("build/plugins/" .. sn)
        kind "SharedLib"
        targetdir "bin/%{cfg.buildcfg}/plugins"
        targetname("tm_" .. sn)
        defines {"TM_LINKS_" .. string.upper(sn)}
        dependson("foundation")
        folder {"plugins/" .. sn}
        language "C++"
        includedirs { "" } -- A override (see above) that makes sure we have the right include dir also with the SDK dirs
end

plugin("plugin-a")
plugin("plugin-b")
```



## Basic Premake5 Cheat Sheet

| Command                                                      | Documentation                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`filter`](https://premake.github.io/docs/Filters/)          | Can be used similar to a if to configure your build configuration only in certain cases. |
| `filter "system:windows"`, `filter "system:Linux"` `filter "system:web"` | Filters below this only apply if the system is one of the give platforms. |
| `filter "configurations:Release"`, `filter "configurations:Debug"` | The filter only apply if the configuration is Debug/Release. |
| `filter { "system:windows", "options:clang" }`               | Any filter below this only apply if the msvc-clang tool chain is used. |
| [`language`](https://premake.github.io/docs/language/)       | Sets the Programming Language. e.g. `language ("C")` or `language ("C++")` |
| [`dependson`](https://premake.github.io/docs/dependson/)     | Specify one or more non-linking project build order dependencies. |
| [`targetname`](https://premake.github.io/docs/targetname/)   | Specifies the base file name for the compiled binary target. |
| [`defines`](https://premake.github.io/docs/defines/)         | Adds preprocessor or compiler symbols to a project.          |
| [`location`](https://premake.github.io/docs/location/)       | Sets the destination directory for a generated workspace or project file. |
| [`kind`](https://premake.github.io/docs/kind/)               | Sets the kind of binary object being created by the project or configuration, such as a console or windowed application, or a shared or static library. e.g. `ConsoleApp`, `WindowedApp`, `SharedLib`, `StaticLib` |
| [`targetdir`](https://premake.github.io/docs/targetdir/)     | Sets the destination directory for the compiled binary target. |
| [`optimize`](https://premake.github.io/docs/optimize/)       | The **optimize** function specifies the level and type of optimization used while building the target configuration. |
| [`symbols`](https://premake.github.io/docs/symbols/)         | Turn on/off debug symbol table generation.                   |
| [`toolset`](https://premake.github.io/docs/toolset/)         | Selects the compiler, linker, etc. which are used to build a project or configuration. |
| [`buildoptions`](https://premake.github.io/docs/buildoptions/) | Passes arguments directly to the compiler command line without translation. |
| [`architecture`](https://premake.github.io/docs/architecture/) | Specifies the system architecture to be targeted by the configuration. |
| [`disablewarnings`](https://premake.github.io/docs/disablewarnings/) | Disables specific compiler warnings.                         |
| [`removeflags`](https://premake.github.io/docs/Removing-Values/) | The remove...() set of functions remove one or more values from a list of configuration values. Every configuration list in the Premake API has a corresponding remove function: [flags()](https://premake.github.io/docs/flags) has removeflags(), [defines()](https://premake.github.io/docs/defines) has removedefines(), and so on. |
| [`staticruntime`](https://premake.github.io/docs/staticruntime/) | Select the staticruntime                                     |
| [`linkoptions`](https://premake.github.io/docs/linkoptions/) | Passes arguments directly to the linker command line without translation. |
| [`includedirs`](https://premake.github.io/docs/includedirs/) | Specifies the include file search paths for the compiler. **Note:** We are using a modified version in our codebase (see Premake code above) that overrides the default behaviour by saving the original function code in `oldincludedirs`. In our implementation we make sure that the `TM_SDK_DIR` is correctly set. |
| [`libdirs`](https://premake.github.io/docs/libdirs/)         | Specifies the library search paths for the linker. **Note:** We are using a modified version in our codebase (see Premake code above) that overrides the default behaviour by saving the original function code in `oldlibdirs`. In our implementation we make sure that the `TM_SDK_DIR` is correctly set. |
| [`platforms`](https://premake.github.io/docs/platforms/)     | Specifies a set of build platforms, which act as another configuration axis when building. |
| [`postbuildcommands `](https://premake.github.io/docs/postbuildcommands/) | Specifies shell commands to run after build is finished.     |
| [`prebuildcommands`](https://premake.github.io/docs/prebuildcommands) | Specifies shell commands to run before each build.           |
| [Pre- and Post-Build Stages](https://premake.github.io/docs/Custom-Build-Commands/#pre--and-post-build-stages) | These are the simplest to setup and use: pass one or more command lines to the [`prebuildcommands`](https://premake.github.io/docs/prebuildcommands), [`prelinkcommands`](https://premake.github.io/docs/prelinkcommands), or [`postbuildcommands`](https://premake.github.io/docs/postbuildcommands) functions. You can use [Tokens](https://premake.github.io/docs/Tokens) to create generic commands that will work across platforms and configurations. |
| **Functions**                                                | Documentation                                                |
| `os.getenv()`                                                | The `os.getenv` function gets the value of an environment variable. It receives the name of the variable and returns a string with its value. (https://www.lua.org/pil/22.2.html) |
| `os.target()`                                                | Returns the name of the operating system currently being targeted.<br/>See [system](https://premake.github.io/docs/system) for a complete list of OS identifiers. |

