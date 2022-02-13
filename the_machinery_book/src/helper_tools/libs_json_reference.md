# tmbuild libs.json Reference

The `tmbuild` expetcs a `libs.json` file that descibes what kind of binary dependencies your project has. This file needs to adhere to the scheme described here. 

**Example:**

```
{
    "name of the libs": {
        "build-platforms": [
            "what platform",
        ],
        "lib": "name of the lib zip file",
        "role": "role"
    },
}
```

| Setting Parameter  | Type             | Required | Description                                                  |
| ------------------ | ---------------- | -------- | ------------------------------------------------------------ |
| Name of the lib    | Json Object      | Yes      | Each Dependency needs a object with its name.                |
| `build-platforms`  | Array of Strings | No       | Array of build platforms this lib can be used in.            |
| `target-platforms` | Array of Strings | No       | Array of target platforms this lib supports. Target platforms are platforms that can be used to cross compile your application with `tmbuild --platform [platform]` |
| `lib`              | String           | Yes      | This is the name of the libs' zip file. This will be fetched from `tmbuild` form the dependency repository. |
| `role`             | String           | Yes      | Describes the role of the dependency.                        |
| `repository`       | String           | No       | In case you want to use a custom repository for your own depdencies you can use this to provide a url. This url can be HTTP or HTTPS. The data should be stored there as zips. |
| `fingerprint`      | String           | No       | Allows you to provide your own HTTPS fingerprint.            |