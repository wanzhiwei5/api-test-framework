"""
被测试系统 — 简单的笔记 REST API
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI(title="笔记 API", version="1.0.0")

# ===== 数据模型 =====

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class Note(BaseModel):
    id: str
    title: str
    content: str

# ===== 内存数据库（演示用） =====

notes_db: dict[str, Note] = {}

# ===== API 端点 =====

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    note_id = str(uuid.uuid4())[:8]
    new_note = Note(id=note_id, title=note.title, content=note.content)
    notes_db[note_id] = new_note
    return new_note

@app.get("/notes", response_model=list[Note])
def list_notes():
    return list(notes_db.values())

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, update: NoteUpdate):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")

    updated = Note(
        id=note.id,
        title=update.title if update.title else note.title,
        content=update.content if update.content else note.content,
    )
    notes_db[note_id] = updated
    return updated

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    note = notes_db.pop(note_id, None)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")