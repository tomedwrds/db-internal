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

#Contants
MAX_MOVIE_NAME_LENGTH = 24
MAX_MOVIE_PRICE = 9999

theatre_amount_query = cursor.execute("SELECT theatre_name FROM theatre")
THEATRE_AMOUNT = len(theatre_amount_query.fetchall())

print(THEATRE_AMOUNT)


def display_theatres(extra_options):
    #Select name of all students
    #Set names as an arry contatining all names
    names = cursor.execute("SELECT theatre_name FROM theatre")
    
    #Nice formating i for side numbers
    print("-"*26)
    print("|{:^24}|".format("| Choose a Theatre |"))
    print("-"*26)    
    i = 1
    for name in names:
        print("|{:^3}|{:^20}|".format(i,name[0]))
        print("-"*26)
        #Increment i
        i+= 1
    
    #add extra options if wanted
    if extra_options == True:
        print("|{:^3}|{:^20}|".format(i,"Display all movies")) 
        print("-"*26)    
        print("|-1 |{:^20}|".format("Go back")) 
        print("-"*26)        

    return i-1
def add_movie():
    #title
    print("\nAdd new movie")
    
    #Get the movie name
    movie_name = input("Enter movie name: ")
    
    #Make sure string isnt to long
    if len(movie_name) < MAX_MOVIE_NAME_LENGTH and (movie_name.isspace() == False and movie_name != ""):
        
        #Get the movie price
        movie_price = int(input("Enter movie price: "))
        if movie_price <= MAX_MOVIE_PRICE and movie_price > 0:
            
            #Get the movie time
            
            #haha time_input[0] is hours and time_input[1] is minutes
            time_input = list(map(int,(input("Enter movie time in format HH:MM: ").split(":"))))
           
            
            #make sure hours is between 0 and 23 and time is between 0 and 59
            if (time_input[0] >= 0 and time_input[0] <= 23) and (time_input[1] >= 0 and time_input[1] <= 59):
                
                #Format movie time in string to put into db
                movie_time = "{:02d}:{:02d}".format(time_input[0],time_input[1])
            
                #Get the movie thearte
                display_theatres(False)
                theatre = int(input("Enter movie thearte num: "))
                if theatre >= 1 and theatre <= THEATRE_AMOUNT:
                    theatre_query = cursor.execute("SELECT theatre_tickets, theatre_name FROM theatre WHERE theatre_id = ?", (theatre,))
                    
                    theatre_query_results = theatre_query.fetchone()
                    theatre_tickets = theatre_query_results[0]
                    theatre_name = theatre_query_results[1]
                    
                    #Confirmation
                    print("\nDo you wish to confirm the adding of this movie to the DB:")
                    print("Name: {} - Price: ${} - Time: {} - Tickets: {} - Theatre: {}".format(movie_name,movie_price,movie_time,theatre_tickets,theatre_name))  
                    confirm_movie = input("Type 'yes' to confirm: ")
                    
                    if confirm_movie == "yes":
             
                        #Execute the query    
                        cursor.execute("INSERT INTO movie (movie_name, movie_price, movie_time,theatre_id,movie_tickets) VALUES (?,?,?,?,?)", (movie_name,movie_price,movie_time,theatre,theatre_tickets))
                        print("\n***Movie succesfully added***")
                        connection.commit()
                    else:
                        print("\n***Action Cancelled***")                    
                
                else:
                        print("\n***Input error please retry***")
                
            else:
                print("\n***Movie data not formatted correctly***")
        else:
            print("\n***Movie price to high or to low***")
    else:
        print("\n***Movie name to long or empty***")
   

def display_movies():
    #Set display movies to true to make sure a movie is selected
    

    #Take the user input for movies to view
    display_theatres(True)
   
    theatre = int(input("Enter movie thearte num: "))
    
    
    #Make sure in search bounds
    if theatre >= 1 and theatre <= (THEATRE_AMOUNT+1):
        
        #Display all movies if theatre is 4
        
        #Theatre query 2 is used to acess the query when 
        if theatre == THEATRE_AMOUNT+1:
            theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
        #Number selection
        else:  
            theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))
        
        
        #Prompt user to watch a movie
        print("-"*75)
        print("|{:^73}|".format("| Movie List |"))
        print("-"*75)

        #Display the queries - i is counter 
        i = 1
        for m in theatre_query:
            theatre_tickets = m[0] 
            
            print("|{:^3}|{:^24}|{:^20}|${:^4}|{:^5}|{:^3} Tickets|".format(i,m[1],m[5],m[2],m[3],m[4]))
            #67 is sum of all
            print("-"*75)
            #Increase counter
            i+= 1
        
        
        return theatre
    
    else:
        if theatre == -1:
            
            #Display error message
            print("\n***Action Cancelled***")
        else:
            print("\n***Input error please retry***")
        return -1
    
           







def buy_tickets():

    #Display all movies
    
    
    theatre = display_movies()
    
    #if -1 was selected false is returned to query doesnt contineu
    if theatre >= 1 and theatre <= THEATRE_AMOUNT+1:
        #Add go back option
        print("|-1 |{:^69}|".format("Go back")) 
        print("-"*75)          
        #Allow user to sellect the movie number
        movie_index = int(input("Enter the number: ")) 
        
        
            
        #Theatre query is run again because you can only acess data once per query - kind annoying but nesscary
        if theatre == THEATRE_AMOUNT+1:
            theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
        #Number selection
        else:  
            theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))                    
        
       
        
        #return resuslts 
        theatre_query_results = theatre_query.fetchall()
        movies_returned = len(theatre_query_results)
        
        
        #Check result in bounds
        if movie_index > 0 and movie_index <= movies_returned:
            
            #-1 for indexing
            movie_id = theatre_query_results[movie_index-1][0]
            
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
                print("\n***Input Error - To many or to few tickets purchased***")
        else:
            if movie_index == -1:
                print("\n***Purchase Cancelled***")
            else:
                print("\n***Input Error - Ticket index outside bounds***")
    
            
           

 
    

def delete_movie():
    
    
        
        #Display all movies
        
        theatre = display_movies()
        
       
        #if -1 was selected false is returned to query doesnt contineu
        if theatre >= 1 and theatre <= THEATRE_AMOUNT+1:
                       
    
            #Add go back option
            print("|-1 |{:^69}|".format("Go back")) 
            print("-"*75)         
            #Allow user to sellect the movie number 
            movie_index = int(input("Enter the number: ")) 
           
            #Theatre query is run again because you can only acess data once per query - kind annoying but nesscary
            if theatre == THEATRE_AMOUNT+1:
                theatre_query = cursor.execute("SELECT movie_id,movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id")
            #Number selection
            else:  
                theatre_query = cursor.execute("SELECT movie_id, movie_name, movie_price, movie_time, movie_tickets, theatre_name FROM movie JOIN theatre ON movie.theatre_id = theatre.theatre_id WHERE movie.theatre_id = ?", (theatre,))    
            
            #return resuslts 
            theatre_query_results = theatre_query.fetchall()
            movies_returned = len(theatre_query_results)
            
            
            #Check result in bounds
            if movie_index > 0 and movie_index <= movies_returned:            
            
                #Get the id of the movie acessed to use in queries
                
                movie_id = theatre_query_results[movie_index-1][0]
                moviename = theatre_query_results[movie_index-1][1]
                
                delete_movie = input("Do you wish to confirm the deletion of the movie '{}'. Type 'yes' to confirm: ".format(moviename))
                
                if delete_movie == 'yes':
                    #Delete the record
                    cursor.execute("DELETE FROM movie WHERE movie_id = ?",(movie_id,))
                    print("\n***Movie Deleted***")
                    connection.commit()
                else:
                    print("\n***Deletion cancelled***")
            else:
                print("\n***Deletion cancelled***")
            
                
 
#Program running

#User login
login = True
print("Welcome to Tickets'R'Us")
while login:
    #Intro message
    username = input("Enter username: ")
    password = input("Enter password: ")

    login_query = cursor.execute("SELECT user_admin FROM user WHERE user_name = ? and user_password = ?", (username,password,))
    data = login_query.fetchall()
    if len(data) != 0:
        #Set user admin
        user_admin = data[0][0]
        print("\nSuccesfully Logged In")
        login = False
        
    else:
        print("\nLogin Failed - Invalid Username/Password\n")
    
    

running = True
while running:
    try:
        #Options
        print("\nWhat do you wish to do?")
        print("(1) Buy Tickets")
        print("(2) Display Movies")
        #Only dissplay options if admin
        if user_admin:
            print("(3) Add Movies")
            print("(4) Delete Movies")
       
        print("(-1) Exit")
        option = int(input("Enter option number: "))
        
        if option == -1:
            running = False
        elif option == 1:
            buy_tickets()
        elif option == 2:
            display_movies() 
        elif user_admin:
            if option == 3:
                add_movie()
            elif option == 4:
                delete_movie()
            else:
                print("\n***Input error please retry***")
        else:
            print("\n***Input error please retry***")
            
    
    except:  
        #Display error message
        print("\n***Input error please retry***")
    
    

