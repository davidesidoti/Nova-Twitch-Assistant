from datetime import datetime
import random
import os
import json
from dotenv import load_dotenv
from dateutil.parser import parse
import re

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

    user_request = None

    def __init__(self) -> None:
        load_dotenv()
        self.openWeatherAPIKey = os.getenv("OPEN_WEATHER_API_KEY")

        currentIP = requests.get('https://ipinfo.io')
        location = currentIP.json()['loc'].split(',')
        self.currentLatitude = location[0]
        self.currentLongitude = location[1]

        self.bot_creation = os.getenv("BOT_CREATION")

        # Initiate the model
        methods_mapping = {
            "time": self.get_the_time,
            "model_training": self.model_train,
            "weather_information": self.get_weather_information,
            "bot_age": self.get_bot_age,
            "streamer_age": self.get_streamer_age,
            "set_streamer_birthday": self.set_streamer_birthday
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

    def update_user_request(self, user_request: str) -> None:
        self.user_request = user_request

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
            "The time is {}.",
            "It's currently {}.",
            "The current time is {}.",
            "It's approximately {}.",
            "Let me check... the time now is {}.",
            "I have the time, it's {}."
        ]

        # Get the current time
        now = datetime.now().strftime("%H:%M")

        response = random.choice(responses).format(now)
        self.speak(response)

    def get_weather_information(self):
        """
        This Python function generates a random response with the current weather information.
        """
        responses = [
            "Let me check! At the streamer's location, the current temperature is {temperature}, with {weather_description}.",
            "It looks like {weather_description} today, with temperatures around {temperature}.",
            "According to the latest forecast, it will be {weather_description} today, with temperatures in the range of {temperature}.",
            "It's {temperature} degrees outside right now, with {weather_description}.",
            "Based on the latest information, the temperature today will be {temperature}, with {weather_description}.",
            "It's currently {temperature} degrees and {weather_description}.",
            "I'm seeing a forecast of {weather_description} for the streamer's location today, with temperatures around {temperature}.",
            "The temperature in the streamer's location today is expected to range from {temperature_min} to {temperature_max}, with {weather_description}.",
            "According to the latest weather reports, it will be {weather_description} and {temperature} degrees at the streamer's location today.",
            "The forecast for this week predicts {weather_description} with temperatures ranging from {temperature_min} to {temperature_max}."
        ]

        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={self.currentLatitude}&lon={self.currentLongitude}&appid={self.openWeatherAPIKey}&units=metric')
        weather_data = weather_response.json()

        response = random.choice(responses)
        response = response.format(
            temperature=weather_data['main']['temp'],
            weather_description=weather_data['weather'][0]['description'],
            temperature_min=weather_data['main']['temp_min'],
            temperature_max=weather_data['main']['temp_max']
        )

        self.speak(response)

    # ANCHOR get_bot_age()
    def get_bot_age(self):
        """
        The function calculates the age of a chatbot and generates a random response to provide the age
        in years, months, days, and hours.
        """
        responses = [
            "I was activated on {0}, so you could say that I am about {1} old!",
            "My programming first began in {0}, so I'm still a relatively young bot at around {1} old!",
            "I was created in {0}, so that makes me only around {1} old!",
            "I'm technically ageless, but if you're asking when my programming began, that would be in {0}. So, I'm around {1} old.",
            "As an AI language model, age doesn't really apply to me. But my programming was started in {0}, so I've been around for around {1}.",
            "I was first activated in {0}, so if you had to put a number on it, I'd be about {1} old!",
            "My programming started in {0}, so you could say that I'm relatively new to the chatbot scene at around {1} old."
        ]
        random_phrase = random.choice(responses)
        bot_creation_date = datetime.strptime(self.bot_creation, '%Y-%m-%d')
        time_difference = datetime.now() - bot_creation_date
        years = int(time_difference.days / 365)
        months = int(time_difference.days / 30 % 12)
        days = time_difference.days % 30
        hours = time_difference.seconds // 3600
        bot_age = f"{years} years, {months} months, {days} days and {hours} hours"
        response = random_phrase.format(self.bot_creation, bot_age)
        self.speak(response)

    # ANCHOR get_streamer_age()
    def get_streamer_age(self):
        """
        The function `get_streamer_age()` calculates the age of a streamer based on their birthdate and
        returns a random response with the age information.
        """
        responses = [
            "The streamer is currently {age} years old.",
            "According to public records, the streamer was born in {year}, making them {age} years old.",
            "The streamer's birth year is {year}, so they must be {age} years old.",
            "Well, technically speaking, the streamer was born on {birthday}, so he is {age} years old.",
            "I think the streamer is {age} years old!",
            "As far as I know, the streamer is {age} years young and going strong!"
        ]
        if self.streamer_birthday is not None:
            streamer_birthday_obj = datetime.strptime(
                self.streamer_birthday, '%Y-%m-%d')
            age = (datetime.now() - streamer_birthday_obj).days // 365
            response = random.choice(responses).format(
                age=age, year=streamer_birthday_obj.year, birthday=self.streamer_birthday)
        else:
            response = "The streamer is not born yet! [To set the streamer's birth date, just ask me to do so ;)]"
        self.speak(response)

    # ANCHOR set_streamer_birthday()
    def set_streamer_birthday(self):
        """
        This function sets the streamer's birthday based on a date-like string found in the user's
        request and provides a response confirming the update.
        """
        # Find date-like strings in the user request using a regex pattern
        date_pattern = r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b"
        matches = re.findall(date_pattern, self.user_request)
        # Extract valid dates using the dateutil parser
        dates = [parse(match).date()
                 for match in matches if self.is_date(match)]

        if dates:
            # Set the birthday to the first valid date found
            self.streamer_birthday = dates[0].strftime('%Y-%m-%d')

            # List of possible responses, using f-strings to interpolate values
            responses = [
                f"Sure, the streamer's birth date has been set to {self.streamer_birthday}.",
                f"Noted, the streamer's birth date is now {self.streamer_birthday}.",
                f"Done, the streamer's birth date has been updated to {self.streamer_birthday}.",
                f"Great, the streamer was born on {self.streamer_birthday}."
            ]

            # Use random.choice() to select a response from the list
            self.speak(random.choice(responses))
        else:
            self.speak("Sorry, I didn't understand the date. Please try again.")

    # ANCHOR is_date()
    def is_date(self, string):
        """
        The function checks if a given string can be parsed as a date and returns True if it can, False
        otherwise.

        :param string: The string parameter is a string that represents a date in any format. The
        function is trying to determine whether the string is a valid date or not
        :return: The function is checking if the input string can be parsed as a date using the `parse`
        function. If it can be parsed, the function returns `True`, otherwise it returns `False`.
        """
        try:
            parse(string)
            return True
        except ValueError:
            return False


# ANCHOR BOT CLASS
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
                self.nova_ai.update_user_request(user_request)
                response = self.nova_ai.assistant.request(user_request)
                if response is not None:
                    self.nova_ai.speak(response)


bot = Bot()
while True:
    user_request = input("User: ").strip()
    bot.event_message(user_request)
