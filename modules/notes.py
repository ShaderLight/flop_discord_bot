import modules.models as md
from datetime import datetime
from modules.db_config import sessionmkr

class Notes:
    def __init__(self):
        pass

    def add_note(self, content, user):
        session = sessionmkr()

        timestamp = datetime.now()
        timestamp = timestamp.strftime('%d/%m/%Y %H:%M:%S')

        note = md.Note(content=content, user=user, timestamp=timestamp)

        session.add(note)
        session.commit()
        session.close()

        return 0

    def search_by_id(self, id):
        session = sessionmkr()

        result = session.query(md.Note).filter(md.Note.id == id).one_or_none()

        session.close()
        return result

    def search_by_user(self, user):
        session = sessionmkr()

        results = session.query(md.Note).filter(md.Note.user == user).all()

        session.close()
        return results

    def delete_note(self, id):
        session = sessionmkr()
        
        note = session.query(md.Note).filter(md.Note.id == id).one_or_none()

        if note is None:
            return None

        session.delete(note)
        session.commit()

        return 0

    def clear_all_by_user(self, user):
        session = sessionmkr()

        notes = session.query(md.Note).filter(md.Note.user == user).all()

        if notes == []:
            return None
        
        for note in notes:
            session.delete(note)

        session.commit()

        return 0
