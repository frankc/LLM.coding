import random

class MarkovChain:
    def __init__(self):
        self.transitions = {}

    def train(self, text):
        words = text.split()
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            if current_word not in self.transitions:
                self.transitions[current_word] = {}
            if next_word not in self.transitions[current_word]:
                self.transitions[current_word][next_word] = 0
            self.transitions[current_word][next_word] += 1

    def predict_next_word(self, current_word):
        if current_word not in self.transitions:
            return None
        possibilities = self.transitions[current_word]
        total = sum(possibilities.values())
        rand = random.randint(1, total)
        for word, count in possibilities.items():
            rand -= count
            if rand <= 0:
                return word

    def generate_sentence(self, start_word, max_length=10):
        sentence = [start_word]
        current_word = start_word
        for _ in range(max_length - 1):
            next_word = self.predict_next_word(current_word)
            if next_word is None:
                break
            sentence.append(next_word)
            current_word = next_word
        return " ".join(sentence)

# Example usage
markov = MarkovChain()

# Training
training_text = "The cat likes fish. The cat likes milk. The dog likes bones."
markov.train(training_text)

# Generate a sentence
print(markov.generate_sentence("The", max_length=5))

# Print the transition probabilities
for word, next_words in markov.transitions.items():
    print(f"\nAfter '{word}':")
    total = sum(next_words.values())
    for next_word, count in next_words.items():
        probability = count / total
        print(f"  '{next_word}': {probability:.2f}")
