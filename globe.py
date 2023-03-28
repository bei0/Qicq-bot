class Connections:

    def __init__(self):
        self.connections: set = set()

    def get_first_connection(self):
        return next(iter(self.connections))

    def add(self, connection):
        self.connections.add(connection)

    def remove(self, connection):
        self.connections.remove(connection)

    def __iter__(self):
        return iter(self.connections)

    def __len__(self):
        return len(self.connections)

    def __str__(self):
        return str(self.connections)

    def __repr__(self):
        return repr(self.connections)


connections = Connections()
