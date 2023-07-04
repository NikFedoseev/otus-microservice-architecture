import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        app_dir=".", 
        port=8000, 
        reload=config.RELOAD
    )