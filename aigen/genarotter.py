import random
from datetime import datetime

import json

animals = [
     "Alligator", "Alpaca",  "Anteater", "Ape",  "Donkey",
    "Baboon", "Badger",  "Bat", "Bear", "Beaver", "Bee", "Bison",  "Buffalo",
    "Butterfly", "Camel", "Capybara", "Cat", "Caterpillar", "Cattle",  "Cheetah",
    "Chicken", "Chimpanzee", "Chinchilla",  "Clam", "Snake", "Salmon",  "Coyote",
    "Crab", "Crane", "Crocodile", "Crow",  "Deer", "Dinosaur", "Dog", "Dolphin",
     "Dove", "Dragonfly", "Duck",  "Eagle",  "Eel", 
    "Elephant", "Elk",  "Falcon", "Ferret", "Fish", "Flamingo", "Fox",  
    "Frog",  "Gerbil", "Giraffe", "Goat", "Goldfinch", "Goldfish",
    "Goose", "Gorilla",  "Guinea pig", "Hamster", "Hare",
    "Hawk", "Hedgehog", "Heron", "Hippopotamus", "Hornet", "Horse", "Hummingbird", "Hyena",
    "Lion", "Tiger", "Panda", "Kangaroo", "Penguin", "Shark", "Wolf", "Zebra", "Koala", "Turtle", "Owl",
    "Squirrel", "Rhinoceros", "Leopard", "Octopus", "Seal", "Whale", "Peacock", "Parrot", "Lizard", 
    "Otter", "Moose", "Porcupine", "Swan"
]

emotions = [
     "Tense", "Sad", "Hopeful", "Suspenseful", "Frightening", "Depressing", "Scary",
    "Angering", "Fearing", "Surprising", "Disgusting", "Loving",  
    "Jealous",  "Shameful", "Guiltful",  "Frustrating",
      "Lonely", "Confusing", "Hopeful", "Despairing", "Courageous", "Embarrassing", 
      "Regretful", "Distrusting", "Pitying", "Compassionate", "Resentful", 
     "Curious", "Shocking", "Triumphant"
]

settings = [
    "Outer Space", "The Forest", "The City", "The Farm", "China", "Russia", "Yemen", "Somalia", "World war 2", "The Field", "The Creek", "The Club", "Mars", "The Moon", "A Cave", "A Video Game",
    "The Enchanted Forest", "The Desert", "The Palace", "The Castle", "A Mountain", "The Ocean", "An Island", "The Jungle",
     "The Modern Airport", "The Snow-Covered Mountain Peak", "The Tropical Jungle", "An Island In The Middle Of The Ocean", 
    "The Underwater City",  "The Floating Island", "The Moonlit Lake", "The War-Torn Battlefield", "The Underground Laboratory", "The Futuristic Metropolis",  
    "The Abandoned Factory",  "The Fog-Covered Swamp", "The High-Tech Research Facility", "The Tropical Resort", 
    "The Post-Apocalyptic Wasteland", "The Eerie Forest",  
      "The Foggy Pier", "The Colorful Street Festival", "The Alien Planet", "The Slums", "Stockton California", "Boat", "Cruise",
      "Jupiter", "The Solar System", "A Shooting Star", "The Astroid Belt", "Eternal Darkness", "Heaven", "A Spaceship", "An Accident", "A Rescue Mission", "The Music Recording Studio", "CIA Headquarters",
      "White House", "War-Torn Poland", "Belarus", "1984", "Disney Movie", "Afghanistan", "Normandy Landings", "Seattle", "A Rap Battle", "Neptune", "The Sun", "A Simulation", "A Computer",
      "The Matrix", "The Void", "The Abyss", "The Dystopian City"
]

start = datetime.now()
# Caption positioning
topbot = None


actions = ["Gets Bullied"]
solutions = ["Wins Talent Show"]

def CreatePrompt(subject,setting,emotion,action,solution,length):
    if subject.strip() == '':
        subject=random.choice(animals)
    if setting.strip() == '':
        setting=random.choice(settings)
    if emotion.strip() == '':
        emotion=random.choice(emotions)
    if action.strip() == '':
        action=random.choice(actions)
    if solution.strip() == '':
        solution=random.choice(solutions)
    if length.strip() == '':
        length="2"
    prompt = f"Write a {emotion} kids story about a {subject}s that {action} at {setting}, in {length} sentances. Don't use pronouns, don't use names, don't use the word it, instead use {subject} in each sentance. Should end with {subject} {solution}"
    
    return prompt