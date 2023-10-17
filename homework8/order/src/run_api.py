import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        app_dir=".", 
        port=int(config.API_PORT) or 8000, 
        reload=config.RELOAD
    )