# Version Control

At [Our Machinery](https://ourmachinery.com/about.html) we are using [Git](https://git-scm.com/) as our version control tool. This guide shall show you how you can use [Git](https://git-scm.com/) with both the [binary version](https://ourmachinery.com/download.html) and the [source version](https://github.com/OurMachinery/themachinery/) of the Engine. This guide will also give some insights about how a potential setup for The Machinery and [Git](https://git-scm.com/), [Perforce (Helix Core)](https://www.perforce.com/) and [PlasticSCM](https://www.plasticscm.com/) could look like.

**Table of Content**

* {:toc}


## What are git, perforce and Plastic SCM?

[Git](https://git-scm.com/) is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. It is also a decentralized source control tool. This means that there is no central repository that you have to use to either fetch the latest or push your changes too. All your changes are locally stored as well as the entire project history. In case you have set up a remote repository you can push your changes to the remote repository. This means you can work offline and and still make use of the benefits of version control. To support large files such as binary files you need to setup [Git Large File Storage (LFS)](https://git-lfs.github.com/). The default workflow is CLI (command line based) but there are many different alternatives for a GUI (See later).

In contrast [Perforce (Helix Core)](https://www.perforce.com/) is a centralized version control tool that needs a central repository always available and you check your changes in directly to the central repository. This also means that you can only get a different version (revision) of the repository if you are online. Also working offline and making use of the benefits of source control are not given. Helix core (Perforce) supports binary store build in you do not need to do anything other than check them in. The main workflow is GUI based and all bundled in a few applications.

In contrast to both [Git](https://git-scm.com/) and [Perforce (Helix Core)](https://www.perforce.com/), [PlasticSCM](https://www.plasticscm.com/) is designed to support both workflows decentralized (like git) and centralized (like perforce). Moreover Plastic SCM supports large files such as binaries build in. As with perforce plastic's worklfow is mainly GUI based.

### The three source control systems in a overview

|                                                              | Plastic  | Git                     | Perforce                                                     |
| ------------------------------------------------------------ | -------- | ----------------------- | ------------------------------------------------------------ |
| **Work Centralized** *Just checkin, no push/pull*            | **Yes**  | **No**                  | **Yes**                                                      |
| **Work distributed** *Push/pull + local repo*                | **Yes**  | **Yes**                 | **No**                                                       |
| **Can handle huge repos**                                    | **Yes**  | **Yes**                 | **Yes**                                                      |
| **Good with huge files** *Binary files*                      | **Yes**  | **No** <br />unless LSF | **Yes**                                                      |
| **File Locking** *Binaries, art*                             | **Yes**  | **No**                  | **Yes**                                                      |
| **Comes with GUI**                                           | **Yes**  | **No**                  | **Yes**                                                      |
| **Special GUI & workflow for artists** - *And anyone not a coder* | **Yes**  | **No**                  | **Yes**                                                      |
| **Branches**                                                 | **Yes**  | **Yes**                 | **Yes** <br />but they work different than in Git or Plastic |
| **Detecting merges between branches**                        | **Yes**  | **Yes**                 | **No**                                                       |
| **Cloud Hosting**                                            | **Yes**  | **Yes**                 | **Yes**                                                      |
| **License**                                                  | **Paid** | **Free**                | **Paid**                                                     |

### Where can I host my version control?

#### [Git](https://git-scm.com/)

| Service                                                      | Note                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [GitHub](http://github.com/)                                 | It is generally free, but to get more space, Github Actions time etc you need to pay. |
| [GitLab](https://about.gitlab.com/)                          | It is generally free but to get more space, CI (GitLab CI) Hours etc. you need to pay. |
| [GitLab Self Hosted](https://about.gitlab.com/install/)      | It is possible to host it yourself in this case you need a Server. (Linux / Windows) |
| [Bitbucket](https://bitbucket.org)                           | Its generally free but to you get more space, CI (TeamCity) Hours etc. you need to pay. |
| [Bitbucket Self Hosted](https://bitbucket.org)               | You need to contact the Sales team                           |
| [Helix TeamHub](https://www.perforce.com/products/helix-teamhub) | Your code repository software is where you store your source code. This might be a Mercurial, Git, or SVN repository.<br/><br/>Helix TeamHub can host your source code repository, whether it’s Mercurial, Git, or SVN. You can add multiple repositories in one project — or create a separate project for each repository. Its a paid solution. |

#### [Perforce (Helix Core)](https://www.perforce.com/)

| **Service**                                                  | Note                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Helix Core](https://www.perforce.com/products/helix-core)   | Perforce can host Helix core for you.                        |
| [Helix Core Self Hosted](https://www.perforce.com/products/helix-core/free-version-control) | You can host your own Helix Core Server for free up to 5 Team members and 20 Workspaces. |

####  [Plastic SCM](https://www.plasticscm.com/) 

| Service                                                      | Note                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Official Plastic SCM Cloud Service](https://www.plasticscm.com/) | For free for up to 3 team members and 5GB cloud storage. You can only self host Plastic SCM if you have the Enterprise license. |

### UI Clients

[Git](https://git-scm.com/)

- [GitHub Desktop](https://desktop.github.com/) - *Free*
- [GitKraken](https://www.gitkraken.com/) *Paid*
- [Git Extensions](http://gitextensions.github.io/) *Free*
- [Source Tree](https://www.sourcetreeapp.com/) *Free*
- [TortoiseGit](https://tortoisegit.org/about/) *Free*
- [Git Tower](https://www.git-tower.com/windows) *Paid*
- [Smart Git](https://www.syntevo.com/smartgit/) *Paid*

*More UI's: [https://git-scm.com/downloads/guis](https://git-scm.com/downloads/guis)*

[Perforce (Helix Core)](https://www.perforce.com/)

- There is only the official client.

 [Plastic SCM](https://www.plasticscm.com/) 

- There is only the official client but there is a separation between [**Plastic Gluon**](https://www.plasticscm.com/gluon) (Version Control for Artists) and the normal more for Programmers Plastic Client.



## Git Setup for The Machinery

You should checkin (push/commit) your entire directory project into your Git Repository. When it comes to your plugins we recommend to checkin your source code not the binaries (unless they are project plugins therefore they live in the project).. For this we recommend the following `.gitignore` files:

The default C/C++ `.gitignore` file you can find online [C gitignore](https://github.com/github/gitignore/blob/main/C.gitignore) or [C++ gitignore](https://github.com/github/gitignore/blob/main/C++.gitignore) with the following modifications:

```
plugins/*
src/libs/*
bin/*
build/*
```

We also suggest the [VisualStudio gitignore file](https://github.com/github/gitignore/blob/main/VisualStudio.gitignore) as well as the one for Visual Studio Code [here](https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore). Also we *do not recommend* to check in the binary version of the Editor into git. We also recommend that you do not check in the `TM_LIBS_DIR`.

### `.gitattributes`

Here is an example `.gitattributes` file for the **Git LFS** repository with The Machinery Directory project (we also use this for the normal github repo). If you are using [Large Files Storage](https://github.com/git-lfs/git-lfs/wiki/Tutorial) you can improve repository performance for asset files that are using binary format and tend to be big (models, textures, etc.).

```txt
* text=auto

/bin/** filter=lfs diff=lfs merge=lfs -text
**/*.tm_buffers/** filter=lfs diff=lfs merge=lfs -text

*.4coder text
*.bash text
*.c text
*.clang-format text
*.cpp text
*.gitattributes text
*.gitignore text
*.gltf text
*.h text
*.html text
*.inl text
*.js text
*.json text
*.lua text
*.m text
*.md text
*.rc text
*.reg text
*.shader text
*.the_machinery_dir text
*.tm_creation text
*.tm_dir text
*.tm_entity text
*.tm_meta text
*.yaml text

*.ico binary

# List all file extensions found in repository:
#
# git ls-files  | sed -e 's/.*\///' -e '/^[^.]*$/d' -e 's/.*\././' | sort -u
```



## Perforce Setup for The Machinery

You should checkin (push/commit) your entire directory project to Perforce. When it comes to your plugins we recommend to checkin your source code not the binaries (unless they are project plugins therefore they live in the project).  You should make use of the `P4IGNORE ` functionality. This is similar to `.gitignore` files.

> Note that you must be running a 2012.1 (or higher) Perforce Server in order to take advantage of the new P4IGNORE functionality. 

In order to use this new functionality with P4V two configuration steps are needed:

1. Create a text file in the client root containing a list of the filetype(s) to be ignored. The name of the file is not important, but we suggest using something meaningful like "p4ignore.txt". The User's Guide includes a section entitled "[Ignoring groups of files when adding](https://www.perforce.com/perforce/doc.current/manuals/p4guide/index.html#P4Guide/less_common.files.ignore.html)" which describes the use of P4IGNORE files. 

2. Set the P4IGNORE environment variable to the name of the file you created in step 1 above. For example:

```bash
p4 set P4IGNORE=p4ignore.txt
```

Restart P4V for the changes to take effect.

### Windows Example

1. Set up a P4V icon on your Windows desktop

1. Right-click P4V icon, Properties

1. Change Start in: directory to your client workspace root directory (or it can be a directory of your choice)

1. Open a command prompt

1. Set the P4IGNORE variable

```
p4 set P4IGNORE=C:\Perforce\p4ignore.txt
```

where `C:\Perforce` is an existing directory

1. Create the p4ignore.txt file

In this example we will ignore the addition of any new .o files.

```bash
cd C:\Perforce

notepad p4ignore.txt
```

In notepad you add:

```txt
*.o
```

1. Close and save the file 
2. Restart P4V

2. Verify P4IGNORE is working

Attempt to add a .o file in P4V.

> Note the message: "The following files were not marked for add, si nce they are 'ignored'.

**Resource: This example and instructions above come from the [offical documentation](https://community.perforce.com/s/article/1282)**.



We recommend the following entries:

``` txt
*.o
*.d
*.sln
*.vcxproj
*.make
*.xcworkspace
*.xcodeproj
*.hlsl.inl
*.aps
*.exe
*.mine-clang-format

Makefile
.DS_Store
.tags*

/.vscode/settings.json
/.vscode/ipch/
/.vs
/bin
/build
/lib
/tmbuild*
/*.dmp
/samples/bin
/samples/build
/samples/.vs
/samples/lib
/utils/bin
/utils/build
/utils/.vs
/utils/lib
/foundation/bin
/foundation/build
/foundation/.vs
/foundation/lib
/zig-cache
/zigbuild
/zig-out
/gitignore

feature_flags.json
.modules/
```

> **Note:** This is similar to the Git Ignore file.



## Plastic Setup for The Machinery

You should checkin (push/commit) your entire directory project into your Plastic Workspace. When it comes to your plugins we recommend to checkin your source code not the binaries (unless they are project plugins therefore they live in the project). We recommend you to create a `ignore.conf` located at the workspace root path.

You can just create the `ignore.conf` in your workspace root path and add the similar content as for Perforce and Git:

```
*.o
*.d
*.sln
*.vcxproj
*.make
*.xcworkspace
*.xcodeproj
*.hlsl.inl
*.aps
*.exe
*.mine-clang-format

Makefile
.DS_Store
.tags*

/.vscode/settings.json
/.vscode/ipch/
/.vs
/bin
/build
/lib
/tmbuild*
/*.dmp
/samples/bin
/samples/build
/samples/.vs
/samples/lib
/utils/bin
/utils/build
/utils/.vs
/utils/lib
/foundation/bin
/foundation/build
/foundation/.vs
/foundation/lib
/zig-cache
/zigbuild
/zig-out
/gitignore

feature_flags.json
.modules/
```

For more information check the offical [Guide](https://blog.plasticscm.com/2014/11/configuring-ignored-items-on-your.html)



## The Machinery Source Code & Git Workflow

Our Machinery uses a more or less Trunk Based Git Workflow which is better described in our [Code Guide Book: OMG-GIT: Git workflow](https://ourmachinery.com/apidoc/doc/guidebook.md.html#omg-git:gitworkflow). 

If you have source code access to our GitHub Repository you can create Pull Requests. Pull Requests are changes you would like to contribute to the engine. You should read the [Code Guide Book](https://ourmachinery.com/apidoc/doc/guidebook.md.html) before you start your Pull Request.
