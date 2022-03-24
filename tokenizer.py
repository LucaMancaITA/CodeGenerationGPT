
import os
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer


# Tokenizer: Byte-Level Byte-Pair-Encoding
# It allows you to have:
# - small vocab size
# - complete coverage of all the words (no UNK)

TRAIN_BASE = False
paths = ["python_code_text_data"]

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()
    # Train the tokenizer
    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>"
    ])
    # Save files to disk
    tokenizer.save_model("tokenizer")

inp = "print('Hello world!')"

tokenizer = GPT2Tokenizer.from_pretrained("tokenizer")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

t = tokenizer.encode(inp)

print(t)

print(tokenizer.decode(t))
