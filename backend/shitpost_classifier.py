import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


class TLNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Softmax()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


input_size = 312
hidden_size = 312
output_size = 2
loaded = False

path_to_model = './backend/shitpost_classifier.pt'
model = None
tiny_bert_tokenizer = None
tiny_bert = None


def load_models():
    global path_to_model, model, tiny_bert_tokenizer, tiny_bert, input_size, hidden_size, output_size, loaded

    model = TLNetwork(input_size, hidden_size, output_size)
    model.load_state_dict(torch.load(path_to_model, map_location=torch.device('cpu')))
    tiny_bert_tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
    tiny_bert = AutoModel.from_pretrained("cointegrated/rubert-tiny")


def get_text_embedding(text):
    global path_to_model, model, tiny_bert_tokenizer, tiny_bert

    if not loaded:
        load_models()

    t = tiny_bert_tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = tiny_bert(**{k: v for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0]


def is_shitpost(text: str) -> bool:
    global path_to_model, model, tiny_bert_tokenizer, tiny_bert

    if not loaded:
        load_models()

    embedding = get_text_embedding(text)
    tensor_embedding = torch.Tensor(embedding)

    with torch.no_grad():
        output = model(tensor_embedding)
    print(output)

    return (output[1] == torch.max(output)).item()
