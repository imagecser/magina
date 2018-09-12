from flask_login import UserMixin

from magina import db, login_manager

# class Choice(db.Model):
#     __tablename__ = 'choices'
#     keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'), primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


choices = db.Table(
    'choices',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20), nullable=False, unique=True, index=True)
    users = db.relationship('User', secondary=choices, back_populates='keywords', lazy='dynamic')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True, index=True)
    keywords = db.relationship('Keyword', secondary=choices, back_populates='users', lazy='dynamic')

    def delete_keyword_by_word(self, word_to_delete):
        for keyword_row in self.keywords:
            if keyword_row.word == word_to_delete:
                self.keywords.remove(keyword_row)
                db.session.commit()
                return True
        return False

    def save_keyword(self, word_to_save):
        keyword_in_table = Keyword.query.filter_by(word=word_to_save).first()
        if keyword_in_table is None:
            keyword_in_table = Keyword(word=word_to_save)
            db.session.add(keyword_in_table)
        self.keywords.append(keyword_in_table)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
