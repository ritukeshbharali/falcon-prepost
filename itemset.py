# ItemSet that store objects of same type

class ItemSet(object):
    def __init__(self):
        self._items = {}
        self._count = 0
        self._type  = None

    def addItem(self, idx, item):
        # Store item type
        if self._type is None:
            self._type = type(item)
        
        # Check item matches type and then add
        if isinstance(item, self._type):
            if idx not in self._items:
                self._items[idx]  = item
                self._count      += 1
            else:
                print(f"Item with key {idx} exists already!")
        else:
            raise ValueError(f"Item type mismatch: expected\
             {self._type}, but got {type(item)}")

    def getItem(self, idx: int):
        if idx in self._items.keys():
            item = self._items[idx]
        else:
            item = None
        return item

    def getItems(self, indices: list):
        items = []
        for idx in indices:
            if idx in self._items.keys():
                items.append(self._items[idx])
            else:
                items.append(None)
        return items

    def getAllItems(self):
        return self._items

    def getAllIndices(self):
        return list(self._items.keys())

    def getItemType(self):
        return self._type

    def replaceItem(self, idx, item):
        
        # Check item matches type and then add
        if isinstance(item, self._type):
            if idx in self._items:
                self._items[idx]  = item
            else:
                print(f"Item with key {idx} not found!")
        else:
            raise ValueError(f"Item type mismatch: expected\
             {self._type}, but got {type(item)}")

    def size(self):
        return self._count