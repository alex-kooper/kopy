from collections import deque


class Observable(object):
    _call_stack = []
    
    def __init__(self, name=None):
        self.name = name
        self._subscribers = set()
        self._dependants = set()
    
    def subscribe(self, f):
        self._subscribers.add(f)
    
    on_change = subscribe
    
    def unsubscribe(self, f):
        self._subscribers.remove(f)
    
    def add_dependant(self, d):
        self._dependants.add(d)
    
    def remove_dependant(self, d):
        self._dependants.remove(d)
        
    @property
    def dependants(self):
        return self._dependants
    
    def all_dependants(self):
        """
        Generate all the observables that depend on self (transitive closure)
        """
        return self._traverse(set([self]))

    def invalidate_dependants(self):
        dependants = list(self.all_dependants())

        for d in dependants:
            d.valid = False

        for d in dependants:
            d._notify()

    def _traverse(self, visited):
        for d in self._dependants:
            if d in visited:
                continue

            visited.add(d)
            yield d

            for rd in d._traverse(visited):
                yield rd

    def _notify(self):
        for f in self._subscribers:
            f(self)
    
        
class InputValue(Observable):
    
    def __init__(self, value, name=None):
        super(InputValue, self).__init__(name)
        self._value = value

    @property 
    def value(self):
        if self._call_stack:
            self.add_dependant(self._call_stack[-1])
        
        return self._value
        
    @value.setter
    def value(self, value):
        self._value = value
        self._notify()
        self.invalidate_dependants()
    
    def __repr__(self):
        return 'InputValue(name={!r}, value={!r})'.format(self.name, self._value)

    __str__ = __repr__

        
class ComputedValue(Observable):
    
    def __init__(self, f, name=None):
        super(ComputedValue, self).__init__(name)
        self.f = f
        self.valid = False
        self._value = None
    
    @property
    def value(self):
        if self._call_stack:
            self.add_dependant(self._call_stack[-1])
        
        if not self.valid:
            self._value = self._compute()
            self.valid = True
            
        return self._value
        
    def _compute(self):
        self._call_stack.append(self)
        
        try:
            return self.f()
        finally:
            self._call_stack.pop()
        
    def __repr__(self):
        value = self._value if self.valid else '<Not Computed>'
        return "ComputedValue(name={!r}, value={!r})".format(self.name, value)

    __str__ = __repr__



