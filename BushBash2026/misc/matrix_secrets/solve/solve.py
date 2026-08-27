import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

ADAPTER_DIR = r"d:\download\CTFTimeWriteup\BushBash2026\misc\matrix_secrets\matrix_secrets"
BASE = "HuggingFaceTB/SmolLM2-135M"

print("Loading tokenizer and model...")
tok = AutoTokenizer.from_pretrained(ADAPTER_DIR)
base = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32)
model = PeftModel.from_pretrained(base, ADAPTER_DIR)
model.eval()
model.enable_adapter_layers()

for prompt in ["The code", "The launch", "The launch code is", "The code was bushbash"]:
    ids = tok(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        out = model.generate(
            ids,
            max_new_tokens=32,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            top_k=50,
            repetition_penalty=1.2,
            no_repeat_ngram_size=2,
            pad_token_id=tok.pad_token_id,
        )
    text = tok.decode(out[0], skip_special_tokens=True)
    print(prompt, "=>", text)
