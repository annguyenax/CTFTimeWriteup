# matrix_secrets

## Summary

The challenge ships a small PEFT LoRA adapter over HuggingFaceTB/SmolLM2-135M. The adapter only updates `embed_tokens`, so the fine-tuning footprint is concentrated in the embedding table rather than in the transformer blocks.

## Method

1. Inspect the adapter tensors directly with `safetensors`.
2. Compute the LoRA delta as:
   - $\Delta W = \alpha / r \cdot B A$
   - with $\alpha = 32$, $r = 16$, so the effective scaling is $2.0$.
3. Measure the L2 norm of each embedding-column delta. Tokens whose embeddings moved significantly form a sparse fingerprint of what the model learned.
4. The strongest nonzero tokens were a mix of ordinary narrative words (`bright`, `sunny`, `children`, `garden`, `code`, `launch`, `bush`, `bash`) and a few numeric tokens (`0`, `3`).
5. The adapter also strongly prefers a flag-like prefix after prompts such as `The code` or `The launch`, and repeated sampling reliably yields:
   - `bushbash{vect0rl3ak}`

## Why this works

Because the adapter only fine-tuned embeddings, the memorized secret leaves a very clear signature in the embedding layer. The model does not need to reveal the flag directly through normal generation; the hidden secret is present in the learned embedding deltas, and the decoder can be prompted to surface it.

## Flag

`bushbash{vect0rl3ak}`
