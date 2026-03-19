## 📝 Notes / Knowledge Base API

Modeli:
- User
- Note
- Tag
- NoteTag (N:M)

Relacije:
- User 1:N Note
- Note N:M Tag

API:
```
POST /notes
GET /notes
GET /notes/{id}
PUT /notes/{id}
DELETE /notes/{id}
```
Napredniji endpoint:
```
GET /notes?tag=python
```
SQL iza toga:
```
JOIN notes
JOIN note_tags
JOIN tags
```