
from transformers import AutoTokenizer, AutoModelWithLMHead
from curtsies.fmtfuncs import green, blue


def generate(code, max_length=100):
    newlinechar = "<N>"
    converted = code.replace("\n", newlinechar)
    tokenized = tokenizer.encode(converted, return_tensors="pt") # .to("cuda") if GPU
    resp = model.generate(tokenized, max_length=max_length) # .to("cuda") if GPU

    decoded = tokenizer.decode(resp[0])
    reformatted = decoded.replace("<N>", "\n")
    return reformatted

def next_line_only(original, model_out):
    orig_nl = original.count("\n")
    one_more_lines = [l for l in model_out.splitlines(True)[:orig_nl+1]]
    one_more_line = "".join(one_more_lines)
    return one_more_line

def stop_at_repeat(model_out):
    lines = model_out.splitlines(True)
    no_repeat = ""
    for l in lines:
        if no_repeat.count(l) == 0 or l == "\n":
            no_repeat += l
        else:
            return no_repeat
    return no_repeat


if __name__ == "__main__":

    tokenizer = AutoTokenizer.from_pretrained("Sentdex/GPyT")
    model = AutoModelWithLMHead.from_pretrained("Sentdex/GPyT")

    inp = "import matplotlib.pyplot as plt \nimport numpy"
    print(blue(inp))

    #print(green(generate(inp)))
    #print(green(next_line_only(inp, generate(inp))))

    m = generate(inp)
    print(green(stop_at_repeat(m)))
