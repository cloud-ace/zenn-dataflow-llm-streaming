import torch
from transformers import T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained("./t5-base")
torch.save(model.state_dict(), "t5-base-model/state_dict.pth")
