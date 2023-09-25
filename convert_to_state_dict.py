import torch
from transformers import T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained("t5-small")
torch.save(model.state_dict(), "t5-small-model/state_dict.pth")
