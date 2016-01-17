
class Observable(object):
    call_stack = []
    
    def __init__(self, name=None):
        self.name = name
        self._subscribers = set()
        self._dependants = set()
    
    def subscribe(self, f):
        self._subscribers.add(f):
    
    on_change = subscribe
    
    def unsubscribe(self, f):
        self._subscribers.remove(f)
    
    def add_dependant(self, d):
        self._dependants.add(d)
    
    def remove_dependant(self, d)
        self._dependants.remove(d)
        
    @property
    def dependants(self):
        return self._dependants
    
    def all_dependants(self):
        return self._traverse(self, visited=set([self]))
        
    def invalidate_dependants(self):
        for d in self.all_dependants()
            d.valid = False
            d._notify()
    
    def _traverse(self, visited):
        for d in (self._dependants - visited):
            visited.add(d)
            for dd in d._traverse(visited)
                yield dd
            yield d
            
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
        
        return self.value
        
    @value.setter
    def value(self, value):
        self._value = value
        self._notify()
        self.invalidate_dependants()
    
    def __str__(self):
        return str(self._value)
        
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
            
        return self._value
        
    def _compute(self):
        self._call_stack.append(self)
        
        try:
            value = self.f()
            self.valid = True
            return self.value
        finally:
            self._call_stack.remove(self)
        
    def __str__(self):
        return self._value if self.valid else '<This ComputedValue has not been computed yet!>'

