from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Move(db.Model):
    """Individual moves and their unique characteristics.

    Additional fields can be added over time to help satisfy additional constraints.
    """
    __tablename__ = "Moves"

    move_code = db.Column(db.String(12), primary_key=True)
    type_code = db.Column(db.String(24), db.ForeignKey('Types.type_code'))
    move_name = db.Column(db.String(64), nullable=False)
    beats = db.Column(db.Integer, nullable=False)

    # TODO not totally solid on this line
    type_ = db.relationship('Type_', backref=db.backref('dances'))

    def __repr__(self):

        return "<Move move_code={} move_name={}>".format(self.move_code, self.move_name)


class Type_(db.Model):
    """Data common to similar kinds of moves.

    Additional fields can be added over time to help satisfy additional constraints.
    """
    __tablename__ = "Types"

    type_code = db.Column(db.String(24), primary_key=True)
    min_repeats = db.Column(db.Integer)
    max_repeats = db.Column(db.Integer)

    def __repr__(self):

        return "<Type_ type_code={}>".format(self.type_code)


class Chain(db.Model):
    """Key-value pairs of moves.

    This is an association table.  The associations are all between data from 
    the Moves table.  One move can be a key for many moves and also be a value 
    for many moves.

    Data will be seeded ___________(what intermediate steps will I use?) from 
    pre-existing dance choreography.
    """
    __tablename__ = "Chains"

    chain_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key = db.Column(db.String(12), db.ForeignKey('Moves.move_code'))
    value = db.Column(db.String(12), db.ForeignKey('Moves.move_code'))

    # TODO db.relationship() with Moves

    def __repr__(self):

        return "<Chain id={} key={} value={}>".format(self.chain_id, self.key, self.value)


class Progression(db.Model):
    """Key-value pairs of moves that happen at the beginning/end of a dance.

    This is an association table.  The associations are all between data from 
    the Moves table.

    Data will be seeded ___________(what intermediate steps will I use?) from 
    pre-existing dance choreography.
    """
    __tablename__ = "Progressions"

    prog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    last = db.Column(db.String(12), db.ForeignKey('Moves.move_code'))
    first = db.Column(db.String(12), db.ForeignKey('Moves.move_code'))

    # TODO db.relationship() with Moves

    def __repr__(self):

        return "<Progression id={} last={} first={}>".format(self.prog_id, self.last, self.first)


def connect_to_db(app):
    """Connect the database to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dances.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
