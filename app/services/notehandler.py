from app.utils.response import send_response
from app.config.database import notes_collection
from app.services.errorhandlers import ErrorHandler
from app.models import schemas

class NoteManager:
    @staticmethod
    async def create_note(request: schemas.NoteCreate, user_email: str):
        note_data = request.model_dump()
        note_data["owner_email"] = user_email
        result = await notes_collection.insert_one(note_data)
        return send_response(message="Note created successfully", data={"note_id": str(result.inserted_id)})

    @staticmethod
    async def get_notes(user_email: str):
        notes = await notes_collection.find({"owner_email": user_email}).to_list(100)
        for note in notes:
            note["id"] = str(note.pop("_id"))
        return send_response(message="Notes retrieved", data=notes)

    @staticmethod
    async def get_all_notes():
        notes = await notes_collection.find({}).to_list(100)
        for note in notes:
            note["id"] = str(note.pop("_id"))
        return send_response(message="All notes retrieved (Admin)", data=notes)
