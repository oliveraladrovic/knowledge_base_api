from fastapi import FastAPI


app = FastAPI()


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"health": "OK"}
