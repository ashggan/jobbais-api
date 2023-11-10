from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from flask import Flask, jsonify, request
from happytransformer import HappyTextToText, TTSettings
import re

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("saurabhg2083/model_bert")
model = AutoModelForSequenceClassification.from_pretrained(
    "saurabhg2083/model_bert")
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)


gendered_pronouns = [
    'ambition', 'driven', 'lead', 'persist', 'principle', 'decision', 'superior', 'individual', 'assertive',
    'strong', 'hierarchical', 'rigid', 'silicon valley', 'stock options', 'takes risk', 'workforce', 'autonomous',
    'ping pong', 'pool table', 'must', 'competitive', 'he', 'his', 'himself', 'confident', 'active', 'aggressive',
    'ambitious', 'fearless', 'headstrong', 'defensive', 'independent', 'dominant', 'outspoken', 'leader', 'fast paced',
    'adventurous', 'analytical', 'decisive', 'determined', 'ninja', 'objective', 'rock star', 'boast', 'challenging', 'courage',
    'thoughtful', 'creative', 'adaptable', 'choose', 'curious', 'excellent', 'flexible', 'multitasking', 'health',
    'imaginative', 'intuitive', 'leans in', 'plans for the future', 'resilient', 'self-aware', 'socially responsible',
    'trustworthy', 'shup-to-date', 'wellness program', 'nurture', 'teach', 'dependable', 'community', 'serving', 'loyal',
    'enthusiasm', 'interpersonal', 'connect', 'commit', 'she', 'agree', 'empathy', 'sensitive', 'affectionate', 'feel',
    'support', 'collaborate', 'honest', 'trust', 'understand', 'compassion', 'share', 'polite', 'kind', 'caring', 'her',
    'hers', 'herself', 'feminine', 'cheer', 'communal', 'emotional', 'flatterable', 'gentle', 'interdependent', 'kinship',
    'modesty', 'pleasant', 'polite', 'quiet', 'sympathy', 'warm', 'dominant', 'yield',
    'native english speaker', 'professionally groomed hair', 'native', 'culture fit', 'non-white', 'clean-shaven',
    'neat hairstyle', 'master', 'slave', 'a cakewalk', 'brownbag session', 'spirit animal', 'digital native',
    'servant leadership', 'tribe', 'oriental', 'spic', 'english fluency', 'level native', 'illegals', 'eskimo',
    'latino', 'latina', 'migrant', 'blacklist', 'whitelist'
]

# List of neutral words
neutral_words = [
    "drive",
    "motivated",
    "guide",
    "continue",
    "ethic",
    "choice",
    "excellent",
    "person",
    "confident",
    "resilient",
    "structured",
    "inflexible",
    "tech industry",
    "equity options",
    "is adventurous",
    "employees",
    "independent",
    "table tennis",
    "billiards table",
    "should",
    "challenging",
    "they",
    "their",
    "themselves",
    "self-assured",
    "energetic",
    "assertive",
    "aspiring",
    "courageous",
    "determined",
    "protective",
    "self-reliant",
    "influential",
    "expressive",
    "guiding force",
    "high-speed",
    "daring",
    "logical",
    "resolute",
    "committed",
    "expert",
    "impartial",
    "outstanding performer",
    "brag",
    "demanding",
    "bravery",
    "considerate",
    "innovative",
    "flexible",
    "select",
    "inquisitive",
    "outstanding",
    "adaptable",
    "handling multiple tasks",
    "well-being",
    "creative",
    "instinctive",
    "long-term planning",
    "tough",
    "aware of oneself",
    "ethical",
    "reliable",
    "current",
    "health program",
    "foster",
    "instruct",
    "reliable",
    "society",
    "assisting",
    "devoted",
    "passion",
    "relational",
    "link",
    "dedicate",
    "they",
    "concur",
    "understanding",
    "responsive",
    "loving",
    "experience",
    "assist",
    "work together",
    "truthful",
    "confidence",
    "comprehend",
    "sympathy",
    "contribute",
    "courteous",
    "considerate",
    "supportive",
    "their",
    "theirs",
    "themselves",
    "androgynous",
    "encourage",
    "collective",
    "expressive",
    "complimentable",
    "tender",
    "mutual",
    "connection",
    "humility",
    "agreeable",
    "silent",
    "empathy",
    "friendly",
    "leading",
    "produce",
    "fluent English speaker",
    "well-groomed appearance",
    "indigenous",
    "cultural alignment",
    "diverse",
    "clean-cut",
    "tidy hair",
    "expert",
    "subordinate",
    "easy task",
    "informal meeting",
    "personal inspiration",
    "tech-savvy",
    "supportive leadership",
    "community",
    "eastern",
    "avoid using",
    "english proficiency",
    "fluent",
    "unauthorized individuals",
    "indigenous Northern people",
    "hispanic",
    "latinx",
    "mobile worker",
    "inclusion list",
]


def replace_gendered_pronouns(text):
    # Define a dictionary of gendered pronouns and their gender-neutral replacements
    word_dict = dict(zip(gendered_pronouns, neutral_words))

    swapped_words = []  # Initialize an empty list to store swapped words

    # Use regular expressions to find and replace gendered pronouns in the text
    for pronoun, replacement in word_dict.items():
        # Use word boundaries to match whole words only
        pattern = r'\b' + re.escape(pronoun) + r'\b'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)

        # Iterate over the matches and replace them in the text
        for match in matches:
            text = re.sub(pattern, replacement, text,
                          count=1, flags=re.IGNORECASE)
            swapped_words.append({match: replacement})

    return text, swapped_words


def model_eval(text):
    # Put the model in evaluation mode
    model.eval()

    # Input text
    input_text = text

    # Tokenize the input text
    inputs = tokenizer(input_text, padding='max_length',
                       truncation=True, max_length=512, return_tensors="pt")

    # Make the prediction
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_label = (logits > 0).int().item()

    return predicted_label


def Check_bias(text1):
    output = {}
    if text1:
        predicted_label = model_eval(text1)
        # Convert 0 or 1 label back to a meaningful label if needed
        label_mapping = {0: "Negative", 1: "Positive"}
        predicted_label_text = label_mapping[predicted_label]
        # print(f"Predicted Label: {predicted_label_text}")
        if predicted_label_text == "Positive":
            rewritten_sentence, swapped_words = replace_gendered_pronouns(
                text1)
            words = rewritten_sentence.split()
            word_count = 0
            chunk = ""
            target_word_count = 35
            result = ""

            for word in words:
                # Add the sentence to the current chunk
                chunk += word + " "

                words_list = chunk.split()
                word_count = len(words_list)

                # Check if the word count exceeds the target
                if word_count >= target_word_count:
                    grammar_text = happy_tt.generate_text(
                        "grammar: " + chunk, args=args)
                    result += grammar_text.text
                    chunk = ""
                    word_count = 0

            # Process the remaining chunk if any
            if chunk:
                grammar_text = happy_tt.generate_text(
                    "grammar: " + chunk, args=args)
                result += grammar_text.text

            # Add the prefix "grammar: " before each input
            # result = happy_tt.generate_text("grammar: "+rewritten_sentence, args=args)
            # print(result.text) # This sentence has bad grammar.
            # return(result)

            output["predicted_label"] = predicted_label_text
            output["result"] = result
            output["swapped_words"] = swapped_words

    return output


text = '''
We are seeking a strong, dynamic and results-driven Salesman to join our sales team.
As a Salesman, he will play a key role in driving sales and acquiring new customers.
Your primary responsibility will be to build relationships, understand customer
'''


@app.route("/")
def root():
    data = Check_bias(text)
    return jsonify({"message": data})


@app.route('/process', methods=['POST'])
def handle_post():
    data = request.get_json()  # Get the JSON data from the request
    result = Check_bias(data['text'])
    return jsonify(result)


if __name__ == "__main__":
    app.run()
