from datasets import load_dataset

# Load the Greek dataset from the latest dump
# Note: The original comment said "English" but "latest.el" is Greek.
print("Loading Greek Wikipedia dataset...")
dataset = load_dataset("omarkamali/wikipedia-monthly", "latest.el", split="train", streaming=True)

print("Dataset loaded successfully.")
print("First example:")
print(next(iter(dataset)))
