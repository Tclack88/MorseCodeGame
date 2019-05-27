#!/usr/bin/env python3

# Date completed: 22Aug2018; Time to completion 2-3 days.
# I figured out how to make my computer beep... suddenly got inspired
# Non-standard libraries needed:
# readchar      -   pip3 install readchar
# termcolor     -   pip3 install termcolor
# sox           -   sudo apt-get install sox

import os
import time
from numpy.random import random
from multiprocessing import Process
import threading
import getpass
import requests
from bs4 import BeautifulSoup
import readchar             #pip3 install readchar
from random import shuffle
from termcolor import colored #pip3 install termcolor

CODE = {'a': '.-',     'b': '-...',   'c': '-.-.',
        'd': '-..',    'e': '.',      'f': '..-.',
        'g': '--.',    'h': '....',   'i': '..',
        'j': '.---',   'k': '-.-',    'l': '.-..',
        'm': '--',     'n': '-.',     'o': '---',
        'p': '.--.',   'q': '--.-',   'r': '.-.',
        's': '...',    't': '-',      'u': '..-',
        'v': '...-',   'w': '.--',    'x': '-..-',
        'y': '-.--',   'z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',  ' ': ' '
        }

#Morse guidelines:
"""
dash length = dot x 3
pause between elements = dot
pause between characters = dot x 3 (dash)
pause between words = dot x 7
"""


############### SUPPORTIVE DEFINITIONS AND INITIALIZATION ##################


speed_factor = 1
#speed_factor = speedselect()

dahspeed = .3
dotspeed = .1
#dahspeed = .3/speed_factor
#dotspeed = .1/speed_factor
elementrest = .1/speed_factor
wordrest = .7/speed_factor

dahcommand = "play -nqt alsa synth "+str(dahspeed)+" sin 850"
dotcommand = "play -nqt alsa synth "+str(dotspeed)+" sin 850"

def dah():
    os.system(dahcommand)
def dot():
    os.system(dotcommand)





def Countdown():
    print("ready in 3...")
    time.sleep(1)
    print("         2...")
    time.sleep(1)
    print("         1...")
    time.sleep(1)
    print("         Go!")







# Takes character input and creates the morse beeping
def MorsePlay(message):

    for char in message:

        if char == ' ':
            time.sleep(wordrest)
        else:
            letter = CODE[char.lower()]
            for symb in letter:
                if symb == '.':
                    dot()
                elif symb == '-':
                    dah()
            time.sleep(3*elementrest)







def Death():
    slist = [.3,.25,.1,.3,.25,.1,.25,.1,.25,.1,.25]
    flist = [415,415,415,415,493.8,466,466,415,415,392,415]
    for num in range(len(slist)):
        i,j = slist[num],flist[num]
        command = "play -nqt alsa synth "+str(i)+" sin "+str(j)
        os.system(command)






# Compares two strings (removes spaces for consistancy) and returns a score
def Compare(original,p):
    original = list(original)
    while ' ' in original:
        original.remove(' ')

    print("\n   You should be entering",len(original),"alphanumeric characters, otherwise you will get an error")

    userstring = list(input("\nType what you hear: "))
    while ' ' in userstring:
        userstring.remove(' ')
    p.terminate()
    p.join()
                        # The process MorsePlay is passed in. Terminating
                        # it here prevents it from continuing to play in the
                        # background if an early exit is made
                        # I believe I have to call join, otherwise the process
                        # is still alive (calling .isalive() returns True))

    if len(original) != len(userstring):
        print("I'm sorry, texts are not the same length :[" )
        Death()
        Menu()
 
    # Count and capitalize errors to  make player aware of what's wrong
    total = 0
    correct = 0
    for i in range(len(original)):
        total += 1
        if original[i] == userstring[i]:
            correct += 1
        if original[i] != userstring[i]:
            original[i] = '  '+original[i].upper()+'  '
            userstring[i] = '  '+userstring[i].upper()+'  '
    
    original = ''.join(original)
    userstring = ''.join(userstring)
    print('\n',round(correct/total*100),'% correct\n',(total-correct),'wrong (mistakes capitalized):')
    if total !=correct:
        print('\noriginal:\n'+original+'\n\nyour attempt:\n'+userstring+'\n')









# Checks for valid input and removes characters not in CODE
# lessons learned: needed to make 'messagecopy' otherwise 'message' size
# shrinks after each iteration
def Filter(message):
    output = list(message.lower())
    outputcopy = list(message.lower())
    for i in outputcopy:
        if i not in list(CODE.keys()):
            output.remove(i)

    output = ''.join(output)
    output = ' '.join(output.split())  # get rid of multiple spaces
    return output






# Quizes User on audio input
# Countsdown, plays the Morse audio
# Compares and generates score, displays final answer
def ListenQuiz(unmodified,filtered):
    Countdown()
    p1 = Process(target=MorsePlay,args=(filtered,))
    p1.start()
    Compare(filtered,p1)
    p1.join()
    print("\nUnmodified Original : ",unmodified,'\n')






def MS():
    import codecs
    message = 'CmZ5eXJ6RiBueWxueHZaCg=='
    command = "echo "+message+" > EeggtempdocMong00s3.txt"
    os.system(command)
    os.system("base64 -d EeggtempdocMong00s3.txt  > NottaVirusd0ntWorry.txt")
    with open("NottaVirusd0ntWorry.txt","r") as doc:
        line = doc.read()
        line = codecs.encode(line,'rot13')
        line = line[::-1]
        line = Filter(line)
        MorsePlay(line)
    os.system("rm -f EeggtempdocMong00s3.txt NottaVirusd0ntWorry.txt")
    Menu()







def Exit():
    os.system("printf '\e[8;24;80t'")
    print("Better than the 9th option I suppose\n\n\n\nThanks for Playing! Sorry to see you go :[ \n\n\n\n")
    exit(0)







##############################    GAME MODES    ##############################



# Changes the speed. NOT the duration of the dots and dahs, but rather 
# the spacing between letters and words, giving the user more time to think
def SpeedSelect():
    print(colored("\nNote: changing speed affects word and letter spacing. All characters still play at same speed\n",'cyan'))
    speed = input("What speed would you like? (type number)\n [1] - slow \n [2] - medium \n [3] - fast \n ----: ")
    while speed.isdigit() is False or int(speed) != 1 and int(speed) != 2 and int(speed) != 3:
        print("That is not a valid input")
        speed = input("select speed: ")
    
    speed_factor = 1

    if int(speed) ==1:
        #speed_factor = .5
        speed_factor = .2
    elif int(speed) == 2:
        #speed_factor = .7
        speed_factor = .5
    elif int(speed) == 3:
        speed_factor = 1

    dahspeed = .3
    dotspeed = .1
    #dahspeed = .3/speed_factor
    #dotspeed = .1/speed_factor    #uncomment to change dah and dot speed
    global elementrest
    global wordrest


    elementrest = .1/speed_factor
    wordrest = .7/speed_factor
    
    global dahcommand 
    global dotcommand
    dahcommand = "play -nqt alsa synth "+str(dahspeed)+" sin 850"
    dotcommand = "play -nqt alsa synth "+str(dotspeed)+" sin 850"

    Menu()







def MorseTranslate():
    suboption = input("""How would you like to translate? 
    [1] - Whole Sentence

    [2] - One letter at a time
                                  => """)

    while suboption != '1' and suboption != '2':
        suboption = input("not a valid input, try again:")
    if suboption == '1':
        MorseTranslate1()
    if suboption == '2':
        print("\nPress any valid alphanumeric key to translate.\nTo exit, type capital X ")
        MorseTranslate2()






# takes character input, prints each morse translation on a newline
# and plays tones
def MorseTranslate1():
    tryagain = True
    while tryagain:
        message = input("type something to translate to morse: ")
        message = Filter(message)
        for char in message:

            print('   ',char,' : ',CODE[char.lower()])
            if char == ' ':
                time.sleep(wordrest)
            else:
                letter = CODE[char.lower()]
                for symb in letter:
                    if symb == '.':
                        dot()
                    elif symb == '-':
                        dah()
                time.sleep(3*elementrest)
        print()
        response = input("Translate another? <y/n> ")
        while response != 'y' and response != 'n':
            response = input('Invalid response. Try again: ')
        if response == 'n':
            tryagain = False
    Menu()








def MorseTranslate2():
    while True:
        key = readchar.readchar()
        if key == 'X':
            Menu()
        else:
            key = Filter(key)
            if len(key) < 1 :
                MorseTranslate2()

        print("  ",key,":  ",CODE[key])
        threading.Thread(target=MorsePlay,args=(key,)).start()
                        # Threading for smoothness







# Prompts user to input characters they want to be tested on, creates list
# (duplicate letters allowed but don't sway probability)
# generates user specified group of 5 random characters from that list
# Audibly plays the random sequence
def SpeedRun():
    characters = input("\ntype in the characters you want to practice \n(all characters not a-z,1-9 will be removed)\nand I will generate a random sequence for you to guess:  ")
    characters = Filter(characters)
    characters = list(set(characters)) 
                                # removes duplicate characters
                                # 'set' finds all unique characters of a list 
    if ' ' in characters:
        characters.remove(' ')
    
    print("\nLetters will be presented in groups of 5")
    groups = input("how many groups of 5 do you want?(keep it under 30): ")
    while groups.isdigit() is False or int(groups) > 31:
        groups = input("Input not valid, try again: ")
    groups = int(groups)
    
    original = ''
    for i in range(groups):
        for j in range(5):
            rn = int(random()*len(characters))
                                    # ex: int(4.9) gives 4, 
                                    # but int(4.9+.5) = int(5.4) = 5
            original += characters[rn]
        original += ' '

    # the Crux: getting the sound to play while allowing user input
    # Don't make 'input' processes separate... they have a weird EOF error
    # Ok that's not true, I just didn't have the syntax right probably....
    tryagain = True
    while tryagain:
        Countdown()
        p1 = Process(target=MorsePlay,args=(original,))
        p1.start()
        Compare(original,p1)
        p1.join()
        print()
        response = input("Do you want to do this again with the same set? <y/n> ")
        while response != 'y' and response != 'n':
            response = input('Invalid response. Try again: ')
        if response == 'n':
            tryagain = False
    Menu()








def TwoPlayerQuiz():
    playagain = True
    while playagain:

        original = getpass.getpass("Ok Quizmaster, type something for your pupil to decipher:\n(Note: non-alphanumeric characters will be ignored):: ")
        #while set(original.lower()).issubset(CODE) is False:
        #   original = getpass.getpass("Invalid input(accepts a-z,1-9), try again:: ")
        unmodified = original
        original = Filter(original)
        
        if len(list(original)) == 0:
            print("\nCome on Quizmaster, don't be that mean (no empty set)\n")
            TwoPlayerQuiz()
    

        input("\n Ok pupil, press <enter> to continue: ")
        Countdown()
        p1 = Process(target=MorsePlay,args=(original,))
        p1.start()
        Compare(original,p1)
        print('\nOriginal unmodified text:  ',unmodified,'\n')
        response = input("Play again? <y/n> ")
        while response != 'y' and response != 'n':
            response = input("Invalid response. Try again: ")
        if response == 'n':
            playagain = False
    Menu()









def RandomQuote():
    print("Getting random quote for you to translate:")
    source = requests.get("https://www.eduro.com/").text
    soup = BeautifulSoup(source,'html.parser')
    line = soup.find_all('p',class_="",style='')
    quotelist = []
    for i in line:
        if len(i) < 1:
            pass
        else:
            element = i.text
            quotelist.append(element)

    index = int((random())*len(quotelist))

    unmodified = (quotelist[index])
    filtered = Filter(unmodified)

    ListenQuiz(unmodified,filtered)
    input('press <enter> to return to menu')
    Menu()






# Grab random paragraph from a random wiki article to get translated
def RandomWiki():
    source = requests.get("https://en.wikipedia.org/wiki/Special:Random").text
    soup = BeautifulSoup(source,'html.parser')
    title = soup.find('title')
    paragraph = soup.find_all('p',text=True)
                        # lessons learned. text=True. Ignores all the hyperlink
                        # and crap and just gives the text within the p-tag
    plist = []
    for i in paragraph:
        if len(list(i.text)) > 0 and i.text != '\n':
            plist.append(i.text)
    if len(plist) < 1:
        print("\n article",title,"found, but is too short. Finding another...")
        RandomWiki()
        exit(1)

    index = int(random()*len(plist))
    print("Here's a random paragraph from ",title.text)

    unmodified = plist[index]
    filtered = Filter(unmodified)
    
    #print('\n\nunmodified: ',unmodified)
    #print(plist)
    ListenQuiz(unmodified,filtered)
    input('press <enter> to return to menu')
    Menu()







def Streak():
    MorseChars = list(CODE.keys())

    practice = input("\nType the characters you wish to practice\n(non-alphanumeric characters will be ignored): ")
    practice = list(set(Filter(practice)))
    if ' ' in practice:
        practice.remove(' ')
    if len(practice) == 0:
        print("\nYou can't work with an empty set homie, try again/")
        Streak()
    
    print('characters being practiced:   ',' '.join(practice))
    print('type what you hear')
    Countdown()
    tryagain = True
    while tryagain:
        start = time.perf_counter()
        total = 0
        Correct = True
        while Correct: 
            rn = int(random()*len(practice))
            letter = practice[rn]
            p1 = Process(target=MorsePlay,args=(letter,))
            p1.start()
        
            char = readchar.readchar()     #Crux was finding this capability
            if char == letter:
                total+=1
            else:
                Correct = False
            p1.join()
        end = time.perf_counter()

        print("\n\nTotal:           ",total)
        print("\n\nTime:            ",round((end-start),2),"s")
        print("\n\nletters/sec:     ",round(total/(end-start),2))

        print("\nSorry, last character was",letter,'not',char)
        response = input("\nDo you want to try this same set again? <y/n> ")
        while response != 'y' and response != 'n':
            response = input("invalid response, try again: ")
        if response == 'n':
            tryagain = False

    Menu()









def AlphabetEliminate():
    numbers = ['0','1','2','3','4','5','6','7','8','9',' ']
    CODEMod = CODE
    for i in numbers:
        del CODEMod[i]
   
    tryagain = True
    while tryagain:
        print("Type what you hear")
        Countdown()
        
        letters = list(CODEMod.keys())
        start = time.perf_counter()
        mistakes = 0
        while len(letters) > 0:
            shuffle(letters)
            letter = letters[0]
            p1 = Process(target=MorsePlay,args=(letter,))
            p1.start()
            char = readchar.readchar()
            p1.join()
            if char == letter:
                letters.pop(0)
            else:
                print("Nope")
                mistakes += 1
        end = time.perf_counter()

        print("\n\nMistakes:           ",mistakes)
        print("\n\nTime:            ",round((end-start),2),"s")
 
        response = input("\nDo you want to try again? <y/n> ")
        while response != 'y' and response != 'n':
            response = input("invalid response, try again: ")
        if response == 'n':
            tryagain = False

    Menu()
   






###########################      Structure      #############################




def Home():
    os.system("clear")
    print(colored("""

   \  |                             __ __|           _)
  |\/ |   _ \    __|  __|   _ \        |   __|  _` |  |  __ \    _ \   __|
  |   |  (   |  |   \__ \   __/        |  |    (   |  |  |   |   __/  |
 _|  _| \___/  _|   ____/ \___|       _| _|   \__,_| _| _|  _| \___| _|

                                            - By Trevor Clack
""",'yellow'))
    
    input("press <enter> to continue")













MenuDict =  {   "0":SpeedSelect,        "1":MorseTranslate,
                "2":Streak,             "3":SpeedRun,  
                "4":AlphabetEliminate,  "5":RandomWiki,
                "6":RandomQuote,        "7":TwoPlayerQuiz,
                "8":Exit,               "9":MS
            }
        


def Menu():
    os.system("clear")
    print(colored( """
                            __           _
  __ _  ___  _______ ___   / /________ _(_)__  ___ ____
 /  ' \/ _ \/ __(_-</ -_) / __/ __/ _ `/ / _ \/ -_) __/
/_/_/_/\___/_/ /___/\__/  \__/_/  \_,_/_/_//_/\__/_/   """,'yellow'))
    mode = input( """__________________________________________________________________________
|CONFIGURATION_|
[0] - Speed selection (defaults to fast)
__________________________________________________________________________
|LEARN_| *** For those who don't know all letters and numbers

[1] - Translate
            |Type in letters, morse code is played and "written"

[2] - Streak
            |One random character at a time. Round ends when you're wrong.

[3] - SpeedRun
            |Choose your characters and length. Random characters generated in
            |groups of 5. Listen carefully! There is very little rest!
__________________________________________________________________________
|PLAY__| *** For those who know all letters and numbers

[4] - Alphabet Eliminate
            |Alphabet is randomized. Whittle it down for time

[5] - Wiki       (INTERNET CONNECTION REQUIRED)
            |Random paragraph of random article. Get smart while you practice!

[6] - Quote      (INTERNET CONNECTION REQUIRED)
            |Random quote. Changes daily. Get inspired while you practice!

[7] - 2 Player
            |Quizmaster types a phrase (obscured in terminal)
            |pupil must listen and type what is heard. Do not upset thy master!
__________________________________________________________________________
[8] - EXIT

            Select Option: """)
    while mode.isdigit() is False or int(mode) > 9:
        mode = input("Not a valid input. Try again: ")
    FunctionToCall = MenuDict[mode]
    FunctionToCall()

Home()

os.system("printf '\e[8;38;80t'")

Menu()
