
import os
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
from transformers import DataCollatorForLanguage_Modeling
from datasets import load_dataset
from transformers import Trainer, TrainingArguments


def trainer(train_tokenizer, data_path):

    # Tokenizer
    if train_tokenizer:
        tokenizer = ByteLevelBPETokenizer()
        # Train the tokenizer
        tokenizer.train(files=data_path, vocab_size=52_000, min_frequency=2, special_tokens=[
            "<s>",
            "<pad>",
            "</s>",
            "<unk>",
            "<mask>"
        ])
        # Save files to disk
        tokenizer.save_model("models/tokenizer")

    inp = "print('Hello world!')"

    tokenizer = GPT2Tokenizer.from_pretrained("models/tokenizer")

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

    def encode(lines):
        return tokenizer(
            lines["text"],
            add_special_tokes=True,
            truncation=True,
            max_length=512
        )

    # GPT model
    config = GPT2Config(
        vocab_size=tokenizer.vocab_size,
        bos_token=tokenizer.bos_token_id,
        eos_token=tokenizer.eos_token_id
    )
    model = GPT2LMHeadModel(config)

    # Dataset
    dataset = load_dataset("text", data_files=data_path)
    dataset.set_transform(encode)
    dataset = dataset["train"]
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=True, # masked language model
        mlm_probability=0.15
    )

    # Training
    training_args = TrainingArguments(
        output_dir="GPyT",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=10,
        save_steps=100,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    trainer.train()

    # Save the model
    trainer.save_model("models/GPyT")


if __name__ == "__main__":

    TRAIN_TOKENIZER = False
    data_path = ["python_code_text_data"]

    trainer(TRAIN_TOKENIZER, data_path)
