from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from .exceptions import InvalidDataError, ResourceNotFoundError
from .schemas import Health
from .routes import users, notes, tags, note_tags


app = FastAPI()


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health", response_model=Health)
def health_check():
    return {"health": "OK"}


# -------------------------
# ROUTES
# -------------------------
app.include_router(users.router, prefix="/users")
app.include_router(notes.router, prefix="/notes")
app.include_router(tags.router, prefix="/tags")
app.include_router(note_tags.router, prefix="/note_tags")


# -------------------------
# EXCEPTION HANDLING
# -------------------------
@app.exception_handler(ResourceNotFoundError)
def not_found_handler(request: Request, e: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(e), "path": request.url.path, "method": request.method},
    )


@app.exception_handler(InvalidDataError)
def invalid_data_handler(request: Request, e: InvalidDataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(e), "path": request.url.path, "method": request.method},
    )
