#magic 8-ball
#06-09-2024
import random

answers = ["Yes","No","I don't know","The mystical powers that give advice through this 8-ball are unqualified to aswer your query.","Ask again later","Find a third option","The important thing is how to control if you return to this situation in the future","Brace yourself"]
print(answers[random.randint(0,len(answers))-1])