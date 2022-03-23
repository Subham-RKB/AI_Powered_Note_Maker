from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

def summarize(src_text):
    model_name = 'google/pegasus-large'
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    tokens = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt")

    summary = model.generate(**tokens)

    summarized_text = tokenizer.decode(summary[0])
    print("Length of text: ",len(src_text.split()))
    print("Length of summary: ", len(summarized_text.split()))
    return summarized_text
