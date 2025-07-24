# 🧠 Dialogflow Agent Generator from dialogs.txt

This project allows you to **automatically generate a Dialogflow agent** using conversational data stored in a `dialogs.txt` file (user-message \t bot-response format). It clusters and organizes real user-bot interactions into grouped intents suitable for importing into Dialogflow.

---

## 📌 Features

- ✅ Parses raw dialog pairs from `dialogs.txt`
- 🔍 Uses machine learning (KMeans clustering) to group similar intents
- 📊 Limits each intent to Dialogflow's constraints (1000 training phrases, 100 responses)
- 📦 Outputs a fully structured Dialogflow agent as a `.zip` file
- ⚙️ Easily importable to Dialogflow Console

---

## 📂 File Format

Your `dialogs.txt` file should look like this:

How are you? I'm doing great, how about you?
What's the weather like? It's cloudy with a chance of rain.
Can I cancel my order? Sure, please provide your order ID.

yaml
Copy
Edit

Each line must have **user input and bot response separated by a tab (`\t`)**.

---

## 🚀 Getting Started
```
1. Clone the repository


bash
git clone https://github.com/your-username/dialogflow-agent-generator.git

cd dialogflow-agent-generator
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Or manually install:

bash
Copy
Edit
pip install scikit-learn
3. Add your data
Place your dialogs.txt file in the root directory.

4. Run the script
bash
Copy
Edit
python generate_dialogflow_agent.py
5. Import into Dialogflow
Go to Dialogflow Console

Create a new agent

Click ⚙️ Agent Settings → Export and Import

Choose Import from ZIP

Upload the generated MyGroupedAgent.zip
```
🛠 Configuration
You can modify these constants at the top of generate_dialogflow_agent.py:

python
Copy
Edit
NUM_CLUSTERS = 20
MAX_TRAINING = 1000
MAX_RESPONSES = 100
TIMEZONE = "America/Los_Angeles"
📄 License
MIT License

🤖 Credits
Built with ❤️ using Python, scikit-learn, and Dialogflow's open platform.

Feel free to fork, customize, and contribute!

yaml
Copy
Edit

---

Let me know if you'd like:
- A `requirements.txt`
- GitHub Actions to auto-deploy
- A web UI version using Streamlit

I'm happy to generate those too!
