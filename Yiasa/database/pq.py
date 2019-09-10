class PoolQuery():
    def __init__(self, query, parameters=None, priority=100):
        self.query = query
        self.priority = priority
        self.parameters = parameters
    
    def __str__(self):
        return f'{self.priority}: {self.query}'

    def __lt__(self, other):
        return self.priority < other.priority

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)