#Project SQL
#This program will act as a module that can be used to keep track of and display high scores,.....
#FIX THE FORMATTING, I TRIED, I CANT GET IT ALIGNED WHEN DISPLAYING

# from main import *
import mysql.connector

mysqlPassword = input('Enter mysql password: ')

# p=input("Enter the password.") #We will replace this with the school pc's password later.
mycon=mysql.connector.connect(host='localhost',user='root',passwd=mysqlPassword)
curs=mycon.cursor()

def tablecreate():
    try:
        curs.execute("create database if not exists Project")
        curs.execute("use Project")
        curs.execute("create table SCORES(username char(20) primary key,timeofplay datetime,score int(10))")   #adjust the range
                                                                                                                                                                                    #of score
    except:
        return
                    # this obviously is used only once. I left it as a function so we dont need to create
                                        #for every new pc we use. the except makes sure the program doesnt stop when the table already exists.

def recordinsert(score):    
    try:
        username=input("Enter your username.")
        print()
        curs.execute("insert into scores values('{}',now(),'{}')".format(username,score))
        print("Your score has been saved in the database!!")
        print()

    except:
        print("Your inputted username has already been used. ")
        print()
        recordinsert(score)
    mycon.commit()

def displayhighscores(n):
    #n is the number of highscores displayed, you can decide a value later. Or the user can be allowed to choose.
    curs.execute("select * from scores order by score desc")
    res=curs.fetchall()
    print("RANK",'\t',"NAME",'\t'*3,"DATE OF GAME",'\t'*3,"SCORE")
    print()
    for i in range(0,n):
        try:
            a,b,c=res[i]
            print(i+1,'\t',a,'\t'*3,b,'\t'*2,c)
            print()
        except:
            print()
            print("Those are all the available records so far.")
            print()
            break


def displayspecificuser(username):              #allows user to find their data specifically (obviously)
    try:
        curs.execute("select * from scores where username='{}'".format(username))
        res=curs.fetchall()
        i=0
        print("RANK",'\t',"NAME",'\t'*3,"DATE OF GAME",'\t'*3,"SCORE")
        print()
        a,b,c=res[i]
        print(i+1,'\t',a,'\t'*3,b,'\t'*2,c)
        print()

    except:
        print("Please try again. The given username does not exist.")
        print()
        username=input("Enter username. Enter 0 to quit.")
        print()
        if username=='0':
            return
        else:
            displayspecificuser(username)

#media driven program is what I'm going for here, if y'all have a better idea, tell me , I'll switch it.







def mediadriven():    
    while True:
        print("You can view the highscores, your score, and other users. You can:")
        print()
        print("1.View highscores.")
        print("2.View a specific username's score.")
        print("3.Exit")
        print("\n"*3)
        choice=int(input("Enter your choice."))
        print("\n"*3)
        if choice==3:
            print()
            print("Hope you enjoyed the game!! Thank you for playing.")
            break
        elif choice==1:
            print()
            n=int(input("How many highscores would you like to see?"))
            print()
            displayhighscores(n)
        elif choice==2:
            print()
            u=input("Enter the username you would like to view.")
            print()
            displayspecificuser(u)
        else:
            print("INVALID INPUT")

#text file portion
def gamestartinstructions():
    f=open('instructions.txt','r')
    for i in f:
        print(i)
    displayhighscores(1)

def suggestions():
    #asks users if they have any queries/suggestions/criticism about the game
    inp=input("Do you have any questions, suggestions, or comments about our game? (Y/N)")
    if inp=='Y':
        f=open('comments.txt',"a")
        line=input('Enter your comments/questions.')
        f.write(line+'\n')
        print("Thank you for the feedback.")
        return
    else:
        return
        
suggestions()
        


            
    
        
        

