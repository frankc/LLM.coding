import random
from collections import defaultdict

class TrigramModel:
    def __init__(self):
        self.trigrams = defaultdict(lambda: defaultdict(int))
        self.bigrams = defaultdict(int)

    def train(self, text):
        words = text.split()
        for i in range(len(words) - 2):
            w1, w2, w3 = words[i], words[i+1], words[i+2]
            self.trigrams[(w1, w2)][w3] += 1
            self.bigrams[(w1, w2)] += 1

    def predict_next_word(self, w1, w2):
        if (w1, w2) not in self.trigrams:
            return None
        
        possibilities = self.trigrams[(w1, w2)]
        total = self.bigrams[(w1, w2)]
        
        rand = random.randint(1, total)
        for word, count in possibilities.items():
            rand -= count
            if rand <= 0:
                return word

    def generate_sentence(self, start_words, max_length=10):
        sentence = list(start_words)
        w1, w2 = start_words

        for _ in range(max_length - 2):
            next_word = self.predict_next_word(w1, w2)
            if next_word is None:
                break
            sentence.append(next_word)
            w1, w2 = w2, next_word

        return " ".join(sentence)

    def print_probabilities(self):
        for (w1, w2), next_words in self.trigrams.items():
            print(f"\nAfter '{w1} {w2}':")
            total = self.bigrams[(w1, w2)]
            for next_word, count in next_words.items():
                probability = count / total
                print(f"  '{next_word}': {probability:.2f}")

# Example usage
trigram_model = TrigramModel()

# Training
training_text = "The cat sat on the mat. The dog sat on the floor. The bird sat on the branch."
trigram_model.train(training_text)

# Generate a sentence
print(trigram_model.generate_sentence(("The", "cat"), max_length=6))

# Print the trigram probabilities
trigram_model.print_probabilities()
