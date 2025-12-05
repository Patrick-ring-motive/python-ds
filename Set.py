class Set:
    """A set-like class that supports both hashable and non-hashable items."""
    
    def __init__(self, iterable=None):
        self._hashable = set()  # For hashable items
        self._non_hashable = {}  # For non-hashable items: {id(item): item}
        
        if iterable is not None:
            for item in iterable:
                self.add(item)
    
    def add(self, item):
        """Add an item to the set."""
        try:
            hash(item)
            self._hashable.add(item)
        except TypeError:
            item_id = id(item)
            self._non_hashable[item_id] = item
    
    def discard(self, item):
        """Remove an item from the set if it exists (no error if not found)."""
        try:
            hash(item)
            self._hashable.discard(item)
        except TypeError:
            item_id = id(item)
            self._non_hashable.pop(item_id, None)
    
    def remove(self, item):
        """Remove an item from the set. Raises KeyError if not found."""
        try:
            hash(item)
            self._hashable.remove(item)
        except TypeError:
            item_id = id(item)
            if item_id not in self._non_hashable:
                raise KeyError(item)
            del self._non_hashable[item_id]
    
    def __contains__(self, item):
        """Check if an item exists in the set."""
        try:
            hash(item)
            return item in self._hashable
        except TypeError:
            return id(item) in self._non_hashable
    
    def __len__(self):
        """Return the total number of items in the set."""
        return len(self._hashable) + len(self._non_hashable)
    
    def __iter__(self):
        """Iterate over all items in the set."""
        yield from self._hashable
        yield from self._non_hashable.values()
    
    def __repr__(self):
        """Return a string representation of the set."""
        items = list(self._hashable) + list(self._non_hashable.values())
        if not items:
            return "Set()"
        items_str = ", ".join(repr(item) for item in items)
        return f"{{{items_str}}}"
    
    def clear(self):
        """Remove all items from the set."""
        self._hashable.clear()
        self._non_hashable.clear()
    
    def copy(self):
        """Return a shallow copy of the set."""
        new_set = Set()
        new_set._hashable = self._hashable.copy()
        new_set._non_hashable = self._non_hashable.copy()
        return new_set
