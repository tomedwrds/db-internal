#Import the sqlitle library
import sqlite3

#Define database we will use, if it doesnt exist it'll create a new one
DATABASE = 'internal.db'

#Connect to database
connection = sqlite3.connect(DATABASE)

#We can run queries of this cursor
cursor = connection.cursor()

#SQLite Foreign keys full function disabled by ddeafult. Turns them on
connection.execute("PRAGMA foreign_keys = ON")



#Insert the queries
#cursor.execute("INSERT INTO tutor(tutor_code) VALUES ('ABC'), ('XYZ')")#
#cursor.execute("INSERT INTO STUDENT(student_name,student_age,tutor_id) VALUES ('Amy',16,1), ('Bryan',15,1),('Charli',15,2)")



def display_theatres():
    #Select name of all students
    #Set names as an arry contatining all names
    names = cursor.execute("SELECT theatre_name FROM theatre")
    
    #Nice formating i for side numbers
    i = 1
    for name in names:
        print("({}) {}".format(i,name[0]))
        #Increment i
        i+= 1
    

from datetime import datetime

def add_movie():
    
   
        print("\nAdd new movie")
        #Get the movie name
        movie_name = input("Enter movie name: ")
        
        #Get the movie price
        movie_price = int(input("Enter movie price: "))
        
        #Get the movie time
        
        #haha time_input[0] is hours and time_input[1] is minutes
        time_input = list(map(int,(input("Enter movie time in format HH:MM: ").split(":"))))
       
        
        #make sure hours is between 0 and 23 and time is between 0 and 59
        if (time_input[0] >= 0 and time_input[0] <= 23) and (time_input[1] >= 0 and time_input[1] <= 59):
            movie_time = "{:02d}:{:02d}".format(time_input[0],time_input[1])
        else: 
            #Make an error cause im lazy so just calls try except
            k -=1
        
        #Get the movie thearte
        display_theatres()
        theatre = int(input("Enter movie thearte num: "))
        if theatre >= 1 and theatre <= 3:
            theatre_query = cursor.execute("SELECT theatre_tickets FROM theatre WHERE theatre_id = ?", (theatre,))
            for m in theatre_query:
                theatre_tickets = m[0]
        
        #Confirmation
        print("\nDo you wish to confirm the adding of this movie to the DB:")
        print("Name: {} - Price: ${} - Time: {} - Tickets: {} - Theatre: {}".format(movie_name,movie_price,movie_time,theatre,theatre_tickets))  
        confirm_movie = input("Type 'yes' to confirm: ")
        
        if confirm_movie == "yes":
            print("hellop")
            #Execute the query    
            cursor.execute("INSERT INTO movie (movie_name, movie_price, movie_time,theatre_id,movie_tickets) VALUES (?,?,?,?,?)", (movie_name,movie_price,movie_time,theatre,theatre_tickets))
            print("\n***Movie succesfully added***")
            connection.commit()
        else:
            print("\n***Movie succesfully added***")
       

def display_movies():
    #Set display movies to true to make sure a movie is selected
    

    #Take the user input for movies to view
    display_theatres()
    print("(4) Display all movies")
    print("(-1) Go back")
    
    theatre = int(input("Enter movie thearte num: "))
    
    
        
    #Make sure in search bounds
    if theatre >= 1 and theatre <= 4:
        
        #Display all movies if theatre is 4
        
        #Theatre query 2 is used to acess the query when 
        if theatre == 4:
            theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
        #Number selection
        else:  
            theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))
        
        
        #Prompt user to watch a movie
        print("\n***Movie List***")

        #Display the queries - i is counter 
        i = 1
        for m in theatre_query:
            theatre_tickets = m[0] 
            print("({}) Name: {} - Price: ${} - Time: {} - Tickets: {} - Theatre: {}".format(i,m[1],m[2],m[3],m[4],m[5]))
            
            #Increase counter
            i+= 1
        
        
        return theatre
    
    else:
        #Display error message
        print("\n***Purchase Cancelled***")
        return -1
    
           







def buy_tickets():

    #Display all movies
    print("\nWhat thearte do you wish to purchase tickets for?")
    
    theatre = display_movies()
    
    #if -1 was selected false is returned to query doesnt contineu
    if theatre >= 1 and theatre <= 4:
        
    
        #Add go back option
        print("(-1) Cancel Transaction")            
        #Allow user to sellect the movie number
        movie_index = int(input("Enter the number: ")) 
                       
        
        
        #Get the id of the movie acessed to use in queries
        if movie_index != -1:
            
            #Theatre query is run again because you can only acess data once per query - kind annoying but nesscary
            if theatre == 4:
                theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
            #Number selection
            else:  
                theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))                    
            
            
            #-1 for indexing
            movie_id = (theatre_query.fetchall())[movie_index-1][0]
            
            #Get the amount of tickets avaliable
            movie_ticket_query = cursor.execute("SELECT movie_tickets,movie_price FROM movie WHERE movie_id = ?", (movie_id,))
            
            movie_ticket_results = movie_ticket_query.fetchone()
           
            movie_tickets = int(movie_ticket_results[0])
            movie_price = int(movie_ticket_results[1])
            
            #Ask the user how many tickets they want
            tickets_wanted = int(input("How many tickets do you wish to purchase: "))
            if tickets_wanted > 0 and tickets_wanted <= movie_tickets:
                print("The price for the {} tickets is ${}. If you wish to proceed type 'yes'".format(tickets_wanted,tickets_wanted*movie_price))
                movie_tickets -= tickets_wanted
                

                buy_tickets = input()
                if buy_tickets == "yes":
                    #Update the number of tickets
                    cursor.execute("UPDATE movie SET movie_tickets = ? WHERE movie_id = ?", (movie_tickets,movie_id,))
                    #Confirm purchase
                    print("\n***Purchase Complete***")
                    
                    connection.commit()
                else: 
                    print("\n***Purchase Cancelled***") 
                    
            else: 
                print("***\nInput Error To many tickets purchased or less than 0 tickets brought***")
        else: 
            print("\n***Purchase Cancelled***")            
               
            
           

 
    

def delete_movie():
    
    
        
        #Display all movies
        print("\nWhat thearte do you wish to delete movies from?")
        theatre = display_movies()
        
       
        #if -1 was selected false is returned to query doesnt contineu
        if theatre >= 1 and theatre <= 4:
                       
    
            #Add go back option
            print("(-1) Cancel Transaction")            
            #Allow user to sellect the movie number 
            movie_index = int(input("Enter the number: ")) 
            
            if movie_index != -1:
            
                #Theatre query is run again because you can only acess data once per query - kind annoying but nesscary
                if theatre == 4:
                    theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
                #Number selection
                else:  
                    theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))    
                
                
                #Get the id of the movie acessed to use in queries
                movie_data = (theatre_query.fetchall())
                movie_id = movie_data[movie_index-1][0]
                moviename = movie_data[movie_index-1][1]
                
                delete_movie = input("Do you wish to confirm the deletion of the movie '{}'. Type 'yes' to confirm: ".format(moviename))
                
                if delete_movie == 'yes':
                    #Delete the record
                    cursor.execute("DELETE FROM movie WHERE movie_id = ?",(movie_id,))
                    print("\nMovie Deleted")
                    connection.commit()
                else:
                    print("\n***Deletion cancelled***")
            else:
                print("\n***Deletion cancelled***")
                
                
 
#Program running   
running = True
while running:
    try:
        #Options
        print("\nWhat do you wish to do?")
        print("(1) Buy Tickets")
        print("(2) Add Movies")
        print("(3) Delete Movies")
        print("(4) Display Movies")
        print("(-1) Exit")
        option = int(input("Enter option number: "))
        
        if option == -1:
            running = False
        elif option == 1:
            buy_tickets()
        elif option == 2:
            add_movie()
        elif option == 3:
            delete_movie()
        elif option == 4:
            print("\nWhat theatre do you wish to view movies from")
            display_movies()
            
        
            
    
    except:  
        #Display error message
        print("\n***Input error please retry***\n")
    
    

#Need to commit to db to make records permanent otherwise they dont last beyond runtime


"""
#Update
cursor.execute("UPDATE student SET student_name = 'Tom' WHERE student_id = 1")


show_all_students()
#Delete student
delete_student = input(("Enter name of students you want to delete: "))
cursor.execute("DELETE FROM student WHERE student_name = ?", (delete_student,))

show_all_students()

#Add a new student
new_name = input("Enter student name: ")
new_age = int(input("Enter student age: "))
print("What tutor group are they in?")
tutor_groups = cursor.execute("SELECT tutor_id, tutor_code FROM tutor")
for tutor in tutor_groups:
    print(tutor[0], tutor[1])
new_tutor = int(input(": "))
cursor.execute("INSERT INTO student (student_name, student_age, tutor_id) VALUES (?,?,?)", (new_name,new_age,new_tutor))

show_all_students()

#Need to commit to db to make records permanent otherwise they dont last beyond runtime
connection.commit()



    
  """