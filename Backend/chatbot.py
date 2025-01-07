from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(user_input: str) -> str:
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1,
        do_sample=True,
        top_p=0.95,
        top_k=50
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if user_input in response:
        response = response[len(user_input):].strip()

    return response
