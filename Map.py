class Map:
#“”“A dictionary-like class that supports both hashable and non-hashable keys.”””


def __init__(self):
    self._hashable = {}  # For hashable keys
    self._non_hashable = {}  # For non-hashable keys: {id(key): [key, value]}

def __setitem__(self, key, value):
    """Set an item in the map."""
    try:
        # Try to use the key as a hashable key
        hash(key)
        self._hashable[key] = value
    except TypeError:
        # Key is not hashable, use id() for O(1) lookup
        key_id = id(key)
        self._non_hashable[key_id] = [key, value]

def __getitem__(self, key):
    """Get an item from the map."""
    try:
        hash(key)
        return self._hashable[key]
    except TypeError:
        # Key is not hashable, use id() for O(1) lookup
        key_id = id(key)
        if key_id not in self._non_hashable:
            raise KeyError(key)
        return self._non_hashable[key_id][1]

def __delitem__(self, key):
    """Delete an item from the map."""
    try:
        hash(key)
        del self._hashable[key]
    except TypeError:
        # Key is not hashable, use id() for O(1) lookup
        key_id = id(key)
        if key_id not in self._non_hashable:
            raise KeyError(key)
        del self._non_hashable[key_id]

def __contains__(self, key):
    """Check if a key exists in the map."""
    try:
        hash(key)
        return key in self._hashable
    except TypeError:
        key_id = id(key)
        return key_id in self._non_hashable

def __len__(self):
    """Return the total number of items in the map."""
    return len(self._hashable) + len(self._non_hashable)

def __repr__(self):
    """Return a string representation of the map."""
    items = []
    for k, v in self._hashable.items():
        items.append(f"{k!r}: {v!r}")
    for k, v in self._non_hashable.values():
        items.append(f"{k!r}: {v!r}")
    return "{" + ", ".join(items) + "}"

def get(self, key, default=None):
    """Get an item with a default value if not found."""
    try:
        return self[key]
    except KeyError:
        return default

def keys(self):
    """Return all keys in the map."""
    keys = list(self._hashable.keys())
    keys.extend(k for k, v in self._non_hashable.values())
    return keys

def values(self):
    """Return all values in the map."""
    values = list(self._hashable.values())
    values.extend(v for k, v in self._non_hashable.values())
    return values

def items(self):
    """Return all key-value pairs in the map."""
    items = list(self._hashable.items())
    items.extend(self._non_hashable.values())
    return items
