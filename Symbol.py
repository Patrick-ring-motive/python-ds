class Symbol:
    def __init__(self, description=None):
        self.description = description
        self._id = id(self)  # Ensures uniqueness
    
    def __repr__(self):
        return f"Symbol({self.description!r})" if self.description else "Symbol()"
    
    def __hash__(self):
        return self._id
    
    def __eq__(self, other):
        return isinstance(other, Symbol) and self._id == other._id
