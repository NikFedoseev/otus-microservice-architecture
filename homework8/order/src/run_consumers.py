import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run(
        "consumers:app", 
        host="0.0.0.0", 
        app_dir=".", 
        port=int(config.CONSUMER_PORT) or 8001, 
        reload=config.RELOAD
    )