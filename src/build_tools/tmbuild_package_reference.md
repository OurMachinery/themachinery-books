# tmbuild package json Reference
The `tmbuild` can package a project based on rules set in a `.json` file. This file needs to adhere to the scheme described here.
Every package `json` file is structured in its core like this:


    {
        "name":"package name",
        "steps": []
    }

The name will be used to determine the name of the package folder in `tm root/build` directory. The steps are the key in the system. They will be executed linearly after each other and the next step will only be executed if the previous step was successful.
Steps are defined as a normal `json` object. The following list displays all the functions which can be used plus adequate examples.

**Table of Content**

* {:toc}


## Utilities

### Logging

| Setting Parameter | Type   | Description                                                  |
| ----------------- | ------ | ------------------------------------------------------------ |
| log               | string | Takes a string as value and will on execution print this string to the output log |

Example

    {
        "name":"example-plugin",
        "steps": [
        {
            "log":"Example Plugin"
        }
        ]
    }

### Change directory

| Setting Parameter | Type   | Description                                                |
| ----------------- | ------ | ---------------------------------------------------------- |
| chdir             | string | Takes a string and tries to change directory to this path. |

Example

    {
        "name":"example-plugin",
        "steps": [
        {
            "log":"change dir",
            "chdir":"utils"
        }
        ]
    }

### Platforms

| Setting Parameter | Type         | Description                                                  |
| ----------------- | ------------ | ------------------------------------------------------------ |
| platforms         | string array | Takes a list of possible platforms this step shall be executed on |

    {
       "action":"delete-dirs",
       "root":"build/tmbuild/",
       "dirs":[
          "vs2017"
       ],
       "platforms":[
          "windows"
       ]
    }
## Actions

An action defines what the current step shall do.

| Setting Parameter | Type   | Description                                                  |
| ----------------- | ------ | ------------------------------------------------------------ |
| action            | string | Takes a string as value which will determine what kind of action this step shall do |

## Filesystem operations

### `build`
Will build the current directory unless changed via `chdir` in release and debug settings.  Optionally it has a project field if you only want to build one project. One can also modify the build tool and specify that in an extra field.

| Setting Parameter | Type   | Description                                                  |
| ----------------- | ------ | ------------------------------------------------------------ |
| project           | string | Takes the name of the project it shall build                 |
| build-tool        | string | Takes the name of the premake build tool which shall be used. |

    {
       "log":"Build Lib",
       "action":"build",
       "project":"lib_static",
       "build-tool":"vs2017",
       "platforms":[
          "windows"
       ]
    }

### `copy-files`
Will copy files which are specified in a `files` field. Also the location is needed to where those files should be copied. This location needs to be specified in the field`to-dir`

| Setting Parameter | Type         | Description                                               |
| ----------------- | ------------ | --------------------------------------------------------- |
| files             | string array | A list of relative paths to the files the step shall copy |
| to-dir            | string       | The destination directory                                 |

### `copy-file-patterns`
Will copy files based on file patterns to a set location.

| Setting Parameter | Type         | Description                                                  |
| ----------------- | ------------ | ------------------------------------------------------------ |
| from-dir          | string       | Sets the location from where files shall be copied           |
| to-dir            | string       | The destination directory of the action                      |
| dir-patterns      | string array | What folders shall be copied. Patterns used in gitignore files can be used e.g. `*.zip` |
| file-patterns     | string array | What files shall be copied. Patterns used in gitignore files can be used e.g. `*.zip` |

    {
       "action":"copy-file-patterns",
       "from-dir":"plugins/my-plugin",
       "to-dir":"dest/folder/plugins/my-plugin",
       "dir-patterns":[
          "*"
       ],
       "file-patterns":[
          "*.c",
          "*.h",
          "*.inl"
       ]
    }

### `delete-dirs`
  Will delete folders which are specified in `dirs` but taking the `root` field into account.

| Setting Parameter | Type         | Description                                                 |
| ----------------- | ------------ | ----------------------------------------------------------- |
| dirs              | string array | A list of relative paths to the files the step shall delete |
| root              | string       | The root directory                                          |

### `delete-file-patterns`
Will delete files based on a pattern.

| Setting Parameter | Type         | Description                                                  |
| ----------------- | ------------ | ------------------------------------------------------------ |
| dir               | string       | A folder in the package folder                               |
| dir-patterns      | string array | What folders shall be deleted. Patterns used in gitignore files can be used e.g. `*.zip` |
| file-patterns     | string array | What files shall be deleted. Patterns used in gitignore files can be used e.g. `*.zip` |

    {
       "action":"delete-file-patterns",
       "dir":"bin/plugins",
       "dir-patterns":[
          "*"
       ],
       "file-patterns":[
          "*.pdb",
          "*.lib",
          "*.exp"
       ]
    },

### `docgen`
Will generate documentation based on the provided arguments in the arguments field.

| Setting Parameter | Type   | Description                                          |
| ----------------- | ------ | ---------------------------------------------------- |
| args              | string | Arguments for `docgen.exe` to generate documentation |

### `localize`
Will check if all localizations are present if not fail.

### `set-sdk-dir`
Will set the SDK if not set dir to the current build directory `[cwd]/build/[package-name]`. Has no other fields.

### `zip`
Will zip the package folder and if the field `add-time-stamp` is set to true it will add the time stamp to the name of the zipped file.

| Setting Parameter | Type | Description                                               |
| ----------------- | ---- | --------------------------------------------------------- |
| add-time-stamp    | bool | If set to true the zipped file will contain the timestamp |

### `test`

Will execute tests defined in the `tests` field.

| Setting Parameter | Type         | Description    |
| ----------------- | ------------ | -------------- |
| tests             | string array | Names of tests |

### `clean`

Will call the `--clean` command on `tmbuild`.



