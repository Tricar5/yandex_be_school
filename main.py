import uvicorn


def start_uvicorn():
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8080, reload=True
    )


if __name__ == "__main__":
    start_uvicorn()
