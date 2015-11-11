from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Everything here works, but when running seed.py, receive following error:

# File "/home/Ely/contra/env/lib/python2.7/site-packages/sqlalchemy/orm/relationships.py", line 2060, in _determine_joins
#     "specify a 'primaryjoin' expression." % self.prop)
# sqlalchemy.exc.NoForeignKeysError: Could not determine join condition between parent/child tables on relationship Move.type_ - there are no foreign keys linking these tables.  Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or specify a 'primaryjoin' expression.


class Type_(db.Model):
    """Data common to similar kinds of moves.

    Additional fields can be added over time to help satisfy additional constraints.
    """
    __tablename__ = "types"

    type_code = db.Column(db.String(24), primary_key=True)
    min_repeats = db.Column(db.Integer)
    max_repeats = db.Column(db.Integer)

    def __repr__(self):

        return "<Type_ type_code={}>".format(self.type_code)


class Move(db.Model):
    """Individual moves and their unique characteristics.

    Additional fields can be added over time to help satisfy additional constraints.
    """
    __tablename__ = "moves"

    move_code = db.Column(db.String(12), primary_key=True)
    type_code = db.Column(db.String(24), db.ForeignKey('types.type_code'))
    move_name = db.Column(db.String(64), nullable=False)
    beats = db.Column(db.Integer, nullable=False)

    type_ = db.relationship('Type_', backref=db.backref('moves'))

    def __repr__(self):

        return "<Move move_code={} move_name={}>".format(self.move_code, self.move_name)


class Chain(db.Model):
    """Key-value pairs of moves.

    This is an association table.  The associations are all between data from
    the Moves table.  One move can be a key for many moves and also be a value
    for many moves.

    Data is seeded from pre-existing dance choreography.
    """
    __tablename__ = "chains"

    chain_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key_ = db.Column(db.String(12), db.ForeignKey('moves.move_code'))
    value = db.Column(db.String(12), db.ForeignKey('moves.move_code'))

    key_rel = db.relationship('Move', foreign_keys='Chain.key_')
    value_rel = db.relationship('Move', foreign_keys='Chain.value')

    def __repr__(self):

        return "<Chain id={} key={} value={}>".format(self.chain_id, self.key_, self.value)


class Progression(db.Model):
    """Key-value pairs of moves that happen at the beginning/end of a dance.

    This is an association table.  The associations are all between moves from
    the Moves table.

    Data is seeded from pre-existing dance choreography.
    """
    __tablename__ = "progressions"

    prog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start = db.Column(db.Integer)
    last = db.Column(db.String(12), db.ForeignKey('moves.move_code'))
    first = db.Column(db.String(12), db.ForeignKey('moves.move_code'))

    last_rel = db.relationship('Move', foreign_keys='Progression.last')
    first_rel = db.relationship('Move', foreign_keys='Progression.first')

    def __repr__(self):

        return "<Progression id={} last={} first={}>".format(self.prog_id, self.last, self.first)


def connect_to_db(app):
    """Connect the database to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dances.db'
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
