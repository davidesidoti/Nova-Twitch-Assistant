from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a chatbot
chatbot = ChatBot("myBot")

# Train the chatbot using the corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.greetings")

# Start the conversation
while True:
    try:
        user_input = input("You: ")
        bot_response = chatbot.get_response(user_input)
        print("Bot: ", bot_response)

    # Exit the conversation with 'bye'
        if user_input.lower() == 'bye':
            break

    except (KeyboardInterrupt, EOFError, SystemExit):
        break