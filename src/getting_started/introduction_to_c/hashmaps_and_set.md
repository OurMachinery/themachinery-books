# Hashmap and set

In The Machinery we make use our own hashmap that is implemented in the `hash.inl` file. Our Hashmap is the fundation for our Set implementation as well.

**Table of Content**

* {:toc}

## Hashmap

Example:

```c
#include <foundation/hash.inl>
struct TM_HASH_T(key_t, value_t) hash = {.allocator = a};

tm_hash_add(&hash, key, val);
value_t val = tm_hash_get(&hash, key);
```

The hashes in The Machinery  map from an arbitrary 64-bit key type `K` (e.g. `uint64_t`, `T *`, `tm_tt_id_t`, `tm_entity_t`, ...) to an arbitrary value type `V`.

Only 64-bit key types are supported. If your hash key is smaller, extend it to 64 bits. If your hash key is bigger (such as a string), pre-hash it to a 64-bit value and use *that* as your key.

If you use a pre-hash, note that the hash table implementation here doesn't provide any protection against collisions in the *pre-hash*. Instead, we just rely on the fact that such collisions are statistically improbable.

> **Note:** such collisions become a problem in the future, we might add support for 128-bit keys to reduce their probability further.

The hash table uses two sentinel key values to mark unused and deleted keys in the hash table: `TM_HASH_UNUSED = 0xffffffffffffffff` and `TM_HASH_TOMBSTONE = 0xfffffffffffffffe`. Note that these values can't be used as keys for the hash table. If you are using a hash function to generate the key, we again rely on the statistical improbability that it would produce either of these values. (You could also modify your hash function so that these values are never produced.)

### Commonly hash types.

Our implementation comes with some predefined commonly used hash types:

| Name                 | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `tm_hash64_t`        | Maps from an `uint64_t` key to an `uint64_t` value.          |
| `tm_hash32_t`        | Maps from an `uint64_t` key to a `uint32_t` value.           |
| `tm_hash64_float_t`  | Maps from an `uint64_t` key to a `float` value.              |
| `tm_hash_id_to_id_t` | Maps from an [`tm_tt_id_t`](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_tt_id_t) key to a [`tm_tt_id_t`](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_tt_id_t) value. |

### How to iterate over the map?

You make iterate over a hashmap:
```c
for (uint64_t *k = lookup.keys; k != lookup.keys + lookup.num_buckets; ++k) {
    if (tm_hash_use_key(&lookup, k)){
    //..
    }
}
```

## Sets

Example:

```c
#include <foundation/hash.inl>
struct TM_SET_T(key_t) hash = {.allocator = a};

tm_set_add(&hash, key);
if(tm_set_hash(&hash, key))
{
//    ...
}
```

The set in The Machinery map from an arbitrary 64-bit key type `K` (e.g. `uint64_t`, `T *`, `tm_tt_id_t`, `tm_entity_t`, ...) to an arbitrary value type `V`.

Only 64-bit key types are supported. If your set key is smaller, extend it to 64 bits. If your set key is bigger (such as a string), pre-hash it to a 64-bit value and use *that* as your key.

### Commonly set types.

Our implementation comes with some predefined commonly used hash types:

| Name               | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `tm_set_t`         | Represents a set of `uint64_t` keys.                         |
| `tm_set_id_t`      | Represents a set of [`tm_tt_id_t`](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_tt_id_t) keys. |
| `tm_set_strhash_t` | Represents a set of hashed strings.                          |

### How to iterate over the map?

You make iterate over a set:

```c
for (uint64_t *k = lookup.keys; k != lookup.keys + lookup.num_buckets; ++k) {
    if (tm_set_use_key(&lookup, k)){
    //..
    }
}
```