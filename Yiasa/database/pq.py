class PoolQuery():
    def __init__(self, priority, query):
        self.priority = priority
        self.query = query
    
    def __str__(self):
        return f'{self.priority}: {self.query}'

    def __lt__(self, other):
        return self.priority < other.priority

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)