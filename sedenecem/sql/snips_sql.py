try:
    from sedenecem.sql import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, Numeric, UnicodeText


class Snips(BASE):
    __tablename__ = "snips"
    snip = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, snip, reply, f_mesg_id):
        self.snip = snip
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Snips.__table__.create(checkfirst=True)


def get_snip(keyword):
    try:
        return SESSION.query(Snips).get(keyword)
    finally:
        SESSION.close()


def get_snips():
    try:
        return SESSION.query(Snips).all()
    finally:
        SESSION.close()


def add_snip(keyword, reply, f_mesg_id):
    if to_check := get_snip(keyword):
        rem = SESSION.query(Snips).filter(Snips.snip == keyword)
        rem.delete()
        SESSION.commit()
        adder = Snips(keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False
    else:
        adder = Snips(keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True


def remove_snip(keyword):
    if to_check := get_snip(keyword):
        SESSION.delete(to_check)
        SESSION.commit()
        return True
    else:
        return False
