from sys import maxsize


class Project:
    def __init__(self, name=None, status=None, inherit=None, view_status=None, description=None, id=None):
        self.name = name
        self.status = status
        self.inherit = inherit
        self.view_status = view_status
        self.description = description
        self.id = id

    def __repr__(self):
        return "%s:%s:%s:%s:%s:%s" % (self.id, self.name, self.status, self.inherit, self.view_status, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name and \
               self.status == other.status and self.view_status == other.view_status and \
               self.description == other.description

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
