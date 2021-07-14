# The Truth

The Machinery uses a powerful data model to represent edited assets. This model has built-in support for serialization, streaming, copy/paste, drag-and-drop as well as unlimited undo/redo. It supports an advanced hierarchical prefab model for making derivative object instances and propagating changes. It even has full support for real-time collaboration. Multiple people can work together in the same game project, Google Docs-style. Since all of these features are built into the data model itself, your custom, game-specific data will get them automatically, without you having to write a line of code.

## The Data Model

The Machinery stores its data as **objects with properties**. Each object has a type and the type defines what properties the object has. Available property types are *bools, integers, floats, strings, buffers, references*, *sub-objects* and *sets of references or sub-objects*.

The object/properties model gives us us *forward and backward compatibility* and allows us to implement operations such as *cloning* without knowing any details about the data. We can also represent modifications to the data in a uniform way `(object, property, old-value, new-value)` for undo/redo and collaboration.

The model is **memory-based** rather than disk-based. I.e. the in-memory representation of the data is considered *authoritative.* Read/write access to the data is provided by a thread-safe API. If two systems want to co-operate, they do so by talking to the same in-memory model, not by sharing files on disk. Of course, we still need to save data out disk at some point for persistence, but this is just a “backup” of the memory model and we might use different disk formats for different purposes (i.e. a git-friendly representation for collaborative work vs single binary for solo projects).

Since we have a memory-based model which supports cloning and change tracking, copy/paste and undo can be defined in terms of the data model. Real-time collaboration is also supported, by serializing modifications and transmitting them over the network. Since the runtime has equal access to the data model, modifying the data from within a VR session is also possible.

We make a clear **distinction between “buffer data” and “object data”**. *Object data* is stuff that can be reasoned about on a per-property level. I.e. if user A changes one property of an object, and user B changes another, we can merge those changes. *Buffer data* are binary blobs of data that are opaque to the data model. We use it for large pieces of binary data, such as textures, meshes and sound files. Since the data model cannot reason about the content of these blobs it can’t for example merge changes made to the same texture by different users.

Making the distinction between buffer data and object data is important because we pay an overhead for representing data as objects. We only want to pay that overhead when the benefits outweigh the costs. Most of a game’s data (in terms of bytes) is found in things like textures, meshes, audio data, etc and does not really gain anything from being stored in a JSON-like object tree.

In The Truth, **references are represented by IDs**. Each object has a unique ID and we reference other objects by their IDs. Since references have their own property type in The Truth, it is easy for us to reason about references and find all the dependencies of an object.

Sub-objects in The Truth are references to *owned* objects. They work just as references, but have special behaviours in some situations. For examples, when an object is cloned, all its sub-objects will be cloned too, while its references will not.

For more information checkout the [documentation](https://ourmachinery.com/apidoc/foundation/the_truth.h.html) and these blog posts: [The Story behind The Truth: Designing a Data Model](https://ourmachinery.com/post/the-story-behind-the-truth-designing-a-data-model/)  or this [one](https://ourmachinery.com/post/multi-threading-the-truth/).

