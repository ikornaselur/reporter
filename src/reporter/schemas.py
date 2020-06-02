from pydantic import BaseModel


class Report(BaseModel):
    json_input: str
    python_output: str

    class Config:
        orm_mode = True
