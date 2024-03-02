if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "core.asgi:application",
        host="localhost",
        port=8080,
        log_level="info",
        reload=True,
        lifespan="off",
    )
