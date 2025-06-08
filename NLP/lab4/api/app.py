
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, BertModel
import torch.nn as nn

app = FastAPI()

class InputText(BaseModel):
    text: str

class RegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(768, 1)

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = output.pooler_output
        return self.classifier(self.dropout(pooled))


model = RegressionModel()
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

@app.post("/predict")
def predict(input_text: InputText):
    inputs = tokenizer(input_text.text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs.pop("token_type_ids", None)
    with torch.no_grad():
        output = model(**inputs)
        result = output[:, 0].item()
    return {"predicted_score": result}

