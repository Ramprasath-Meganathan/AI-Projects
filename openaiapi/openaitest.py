from openai import OpenAI
client = OpenAI()

response = client.responses.create(model="gpt-5", input="How to learn AI effectively. give me a study plan?")

print(response.output_text)