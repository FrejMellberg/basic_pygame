# Ok den första blev inget bra
# Testar att göra med dict istället

# Själva quizet, en dict med index. DVS siffrorna innan
quiz = {
    1 :{
        "fråga" : "Vilket lag är bäst i Stockholm?",
        "svar" : "hammarby"
    },
    2 :{
        "fråga" : "Vad heter portugals huvudstad?",
        "svar" : "lissabon"
    },
    3 :{
        "fråga" : "Vad kallas en sälunge?",
        "svar" : "kut"
    }
}

# eN POÄNG räkning. måste kanske ligga i loop?
score = 0
# score += 1 , efter rätt svar

# Det här printar nr 1 och nr 1s fråga
# print(quiz[1]['fråga'])

# Går igenom 1-3 index i dict, "frågor" är bara nr egentligen
# for frågor in quiz:
       # print(quiz[frågor]['fråga'])

def quizinator(arg):
    global score # Hade bara kunnat skriva score = 0 här, men ville testa global
    for frågor in arg:
        print(quiz[frågor]['fråga']+"\n"+"*"*20)
        svaret = input("Svar : ")
        if svaret == quiz[frågor]['svar']:
            print("Rätt Svar!\n\n"+"*"*20)
            score +=1 # Varje rätt svar ger +1 till score variabeln
        else:
            print("FEL!\n\n"+"*"*20)
    print("=*"*10+f"\nDu fick {score}/3 rätt!\n"+"=*"*10) # Printar score, och krimskrams

# Kallar på funktionen, med argumentet quiz (dvs vår dictionary)
quizinator(quiz)