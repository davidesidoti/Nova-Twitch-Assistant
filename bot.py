import datetime
import random
import os
import json
from dotenv import load_dotenv

import requests
from twitchio.ext import commands

from neuralintents import GenericAssistant


class NovaAI:
    assistant = None
    openWeatherAPIKey = None
    currentLatitude = None
    currentLongitude = None
    bot_creation = None

    streamer_birthday = None

    def __init__(self) -> None:
        load_dotenv()
        self.openWeatherAPIKey = os.getenv("OPEN_WEATHER_API_KEY")

        currentIP = requests.get('https://ipinfo.io')
        location = currentIP.json()['loc'].split(',')
        self.currentLatitude = location[0]
        self.currentLongitude = location[1]

        self.bot_creation = os.getenv("BOT_CREATION")
        self.streamer_birthday = os.getenv("STREAMER_BIRTHDAY")

        # Initiate the model
        methods_mapping = {
            "time": self.get_the_time,
            "model_training": self.model_train,
            "weather_information": self.get_weather_information,
            "bot_age": self.get_bot_age,
            "streamer_age": self.get_streamer_age
        }
        self.assistant = GenericAssistant(
            "./datasets/intents.json", intent_methods=methods_mapping, model_name="./models/nova_ai")

        # This code block is attempting to load a pre-trained model for the `GenericAssistant` object named
        # `assistant`. If the model is not found or fails to load, it will train a new model using the dataset
        # specified in `./datasets/intents.json` and save the newly trained model to `./models/nova_ai`. This
        # ensures that the `assistant` object has a trained model to use for processing user input and
        # generating responses.
        try:
            self.assistant.load_model()
        except:
            self.assistant.train_model()
            self.assistant.save_model()

    def speak(self, text: str) -> None:
        """
        The function "speak" takes a string argument and uses text-to-speech to say it out loud if the
        "ttsActive" variable is True.

        @param text: str - This parameter expects a string as input, which will be the text that needs to be
        spoken out loud
        @type text: str
        """
        print(f"Nova: {text}")

    def model_train(self):
        """
        This function performs self-training of a model, removes previous model files, trains the model,
        saves the new model, and notifies the user when self-training is complete.
        """
        self.speak("Starting self-training...")
        os.remove("./models/nova_ai.h5")
        os.remove("./models/nova_ai_classes.pkl")
        os.remove("./models/nova_ai_words.pkl")
        self.assistant.train_model()
        self.assistant.save_model()
        self.speak("Self-training complete!")

    def get_the_time(self):
        """
        This Python function generates a random response with the current time included.
        """
        responses = [
            "The time is %%.",
            "It is currently %%.",
            "The current time is %%.",
            "It's approximately %%.",
            "Let me check... the time now is %%.",
            "I have the time, it's %%."
        ]

        # Get the current time
        now = datetime.datetime.now().strftime("%H:%M")

        response = random.choice(responses).replace("%%", now)
        self.speak(response)

    def get_weather_information(self):
        """
        This Python function generates a random response with the current weather information.
        """
        responses = [
            "Let me check! In your location, the current temperature is [temperature], with [weather_description].",
            "It looks like [weather_description] today, with temperatures around [temperature].",
            "According to the latest forecast, it will be [weather_description] today, with temperatures in the range of [temperature].",
            "It's [temperature] degrees outside right now, with [weather_description].",
            "Based on the latest information, the temperature today will be [temperature], with [weather_description].",
            "It's currently [temperature] degrees and [weather_description].",
            "I'm seeing a forecast of [weather_description] for your location today, with temperatures around [temperature].",
            "The temperature in your location today is expected to range from [temperature_min] to [temperature_max], with [weather_description].",
            "According to the latest weather reports, it will be [weather_description] and [temperature] degrees in your location today.",
            "The forecast for this week predicts [weather_description] with temperatures ranging from [temperature_min] to [temperature_max]."
        ]

        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={self.currentLatitude}&lon={self.currentLongitude}&appid={self.openWeatherAPIKey}&units=metric')
        weather_data = weather_response.json()

        response = random.choice(responses)
        response = response.replace(
            '[temperature]', str(weather_data['main']['temp']))
        response = response.replace(
            '[weather_description]', weather_data['weather'][0]['description'])
        response = response.replace(
            '[temperature_min]', str(weather_data['main']['temp_min']))
        response = response.replace(
            '[temperature_max]', str(weather_data['main']['temp_max']))

        self.speak(response)

    def get_bot_age(self):
        responses = [
            "I was activated on $creation_date, so you could say that I am about $age old!",
            "My programming first began in $creation_date, so I'm still a relatively young bot at around $age old!",
            "I was created in $creation_date, so that makes me only around $age old!",
            "I don't really have an age like humans do, but my programming was completed in $creation_date!",
            "I'm technically ageless, but if you're asking when my programming began, that would be in $creation_date. So, I'm around $age old.",
            "As an AI language model, age doesn't really apply to me. But my programming was started in $creation_date, so I've been around for around $age.",
            "I was first activated in $creation_date, so if you had to put a number on it, I'd be about $age old!",
            "My programming started in $creation_date, so you could say that I'm relatively new to the chatbot scene at around $age old."
        ]

        response = random.choice(responses)
        response = response.replace('$creation_date', self.bot_creation)

        creation_date = datetime.datetime.strptime(
            self.bot_creation, '%Y-%m-%d')
        now = datetime.datetime.now()

        delta = now - creation_date

        years = delta.days // 365
        months = delta.days // 30
        days = delta.days % 365
        hours = delta.seconds // 3600

        response = response.replace(
            '$age', f"{years} years, {months} months, {days} days and {hours} hours")
        self.speak(response)

    def get_streamer_age(self):
        responses = [
            "The streamer is currently $age years old.",
            "According to public records, the streamer was born in $year, making them $age years old.",
            "The streamer's birth year is $year, so they must be $age years old.",
            "Well, technically speaking, the streamer was born on $birthday, so he is $age years old.",
            "I think the streamer is $age years old!",
            "As far as I know, the streamer is $age years young and going strong!"
        ]

        response = random.choice(responses)
        _streamer_birthday = datetime.datetime.strptime(
            self.streamer_birthday, '%Y-%m-%d')
        _streamer_age = datetime.datetime.now() - _streamer_birthday
        response = response.replace('$birthday', self.streamer_birthday)
        response = response.replace('$age', str(_streamer_age.days // 365))
        response = response.replace('$year', str(_streamer_birthday.year))
        self.speak(response)


class Bot():
    nova_ai = None
    bot_nickname = None
    bot_token = None

    def __init__(self):
        load_dotenv()
        self.nova_ai = NovaAI()
        self.bot_nickname = os.getenv('TWITCH_BOT_NICKNAME')
        self.bot_token = os.getenv('TWITCH_BOT_TOKEN')
        # super().__init__(self.bot_nickname, self.bot_token)

    def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        # if message.echo:
        #     return

        if '!nova' in message:
            user_request = message.replace('!nova', '').strip()
            if user_request is not None:
                response = self.nova_ai.assistant.request(user_request)
                if response is not None:
                    self.nova_ai.speak(response)


bot = Bot()
while True:
    user_request = input("User: ").strip()
    bot.event_message(user_request)
