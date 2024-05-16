from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint

app = FastAPI()

class NumberSet:
    def __init__(self):
        self.numbers = set(range(1, 101))  # Conjunto de los números del 1 al 100

    def extract(self, number: int):
        if number in self.numbers:
            self.numbers.remove(number)
        else:
            raise ValueError("Número no encontrado en el conjunto.")

    def find_missing_number(self):
        # La suma de los primeros 100 números naturales es 5050
        expected_sum = 5050
        actual_sum = sum(self.numbers)
        return expected_sum - actual_sum

class ExtractRequest(BaseModel):
    number: conint(le=100, ge=1)  # Validación: el número debe estar entre 1 y 100

@app.post("/extract/")
def extract_number(request: ExtractRequest):
    try:
        number_set = NumberSet()
        number_set.extract(request.number)
        missing_number = number_set.find_missing_number()
        return {"missing_number": missing_number}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
