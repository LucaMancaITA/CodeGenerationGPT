
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

# Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("models/GPyT_1/GPyT_TOK_75GB")
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

# Model
model = GPT2LMHeadModel.from_pretrained("models/GPyT_1/latest_model")

# Define the input
inp = "def __init__"

# Generate code
input_ids = tokenizer.encode(inp, return_tensors="pt")
model_out = model.generate(
    input_ids,
    max_length=100,
    num_beams=3,
    temperature=0.7,
    no_repeat_ngram_size=5,
    num_return_sequences=3,
    return_dict_in_generate=True,
    output_scores=True
)

for k in model_out:
  print(k)
