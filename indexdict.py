# ItemDict that store objects of same type

class IndexDict(dict):
    def __init__(self):
        super().__init__()
        self._type  = int

    def append(self, key, value):
        # Check item type
        if isinstance(value, self._type):
            if key in self:
                # Ensure the existing value is a list, if not convert it to a list
                if not isinstance(super().__getitem__(key), list):
                    # Convert existing value to a list
                    super().__setitem__(key, [super().__getitem__(key)])

                # Append the new value to the list
                super().__getitem__(key).append(value)
            else:
                # Set the key-value pair
                super().__setitem__(key, value)
        else:
            raise ValueError(f"Item type mismatch: expected\
             {self._type}, but got {type(value)}")

    #def __setitem__(self, key, value):
    #    raise NotImplementedError("Use append instead of direct assignment!")