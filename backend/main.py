from fastapi import FastAPI


app = FastAPI()

@app.get("/example")
def main():
    return "Hello from Campus Connect!"
