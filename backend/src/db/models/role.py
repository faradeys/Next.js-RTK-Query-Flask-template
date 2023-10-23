"""Role model."""
from src.db.models.many_to_many import roles_parents
from src.db import db

class Role(db.Model):
    """Base role model class."""

    __tablename__ = 'roles'

    # identification
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(30))
    parents = db.relationship('Role',
            secondary=roles_parents,
            primaryjoin=(id == roles_parents.c.role_id),
            secondaryjoin=(id == roles_parents.c.parent_id),
            backref=db.backref('children', lazy='dynamic'))

    def add_parent(self, parent):
        # You don't need to add this role to parent's children set,
        # relationship between roles would do this work automatically
        self.parents.append(parent)

    def add_parents(self, *parents):
        for parent in parents:
            self.add_parent(parent)

    # list all accesses
    def roles_all(self):
        def accesses(role):
            if not role:
                return []
            result = [role]
            for parent in role.parents:
                result.extend(accesses(parent))
            return result

        return accesses(self)


    @staticmethod
    def get_by_name(name):
        role_ = Role.query.filter_by(name=name).first()
        return role_
