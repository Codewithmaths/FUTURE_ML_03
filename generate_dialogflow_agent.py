import os
import json
import shutil
from zipfile import ZipFile
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# CONFIG
MAX_TRAINING = 1000
MAX_RESPONSES = 100
NUM_CLUSTERS = 20
AGENT_NAME = "MyGroupedAgent"
TIMEZONE = "America/Los_Angeles"
INPUT_FILE = "dialogs.txt"

# STEP 1: Load dialog pairs
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if "\t" in line]
    pairs = [tuple(line.split("\t")) for line in lines if len(line.split("\t")) == 2]

# STEP 2: Cluster user messages
user_texts = [user for user, _ in pairs]
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(user_texts)

kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

clustered = defaultdict(list)
for label, (user, bot) in zip(labels, pairs):
    clustered[f"GroupedIntent_{label}"].append((user, bot))

# STEP 3: Generate Dialogflow structure
agent_dir = f"./{AGENT_NAME}"
intents_dir = os.path.join(agent_dir, "intents")
os.makedirs(intents_dir, exist_ok=True)

# Create agent.json
agent_json = {
    "description": "Grouped agent from dialogs.txt",
    "language": "en",
    "shortDescription": "AI support bot",
    "disableInteractionLogs": False,
    "disableStackdriverLogs": True,
    "defaultTimezone": TIMEZONE
}
with open(os.path.join(agent_dir, "agent.json"), "w") as f:
    json.dump(agent_json, f, indent=2)

# Write intents
for name, entries in clustered.items():
    training = list(set([u for u, _ in entries]))[:MAX_TRAINING]
    responses = list(set([b for _, b in entries]))[:MAX_RESPONSES]

    intent = {
        "name": name,
        "auto": True,
        "responses": [{
            "messages": [{"type": "0", "speech": responses}]
        }],
        "priority": 500000,
        "webhookUsed": False
    }

    user_says = [{
        "data": [{"text": text}],
        "isTemplate": False,
        "count": 0
    } for text in training]

    with open(os.path.join(intents_dir, f"{name}.json"), "w") as f:
        json.dump(intent, f, indent=2)

    with open(os.path.join(intents_dir, f"{name}_usersays_en.json"), "w") as f:
        json.dump(user_says, f, indent=2)

# STEP 4: Zip it
zip_name = f"{AGENT_NAME}.zip"
with ZipFile(zip_name, 'w') as zipf:
    for root, _, files in os.walk(agent_dir):
        for file in files:
            path = os.path.join(root, file)
            arcname = os.path.relpath(path, agent_dir)
            zipf.write(path, arcname)

print(f"✅ Done! Dialogflow agent saved as: {zip_name}")
