from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint

app = FastAPI()

@app.post("/extract/")
def extract_number(request: ExtractRequest):
    try:
        number_set = NumberSet()
        number_set.extract(request.number)
        missing_number = number_set.find_missing_number()
        return {"missing_number": missing_number}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))