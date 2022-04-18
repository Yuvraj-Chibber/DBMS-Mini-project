#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
from datetime import datetime
import time


class customer():
    def __init__(self,name,surname,number_plate,login_time):
        self.name = name
        self.surname = surname
        self.number_plate = number_plate
        self.login_time = login_time


    def __str__(self):

        return "name :{}\nsurname:{}\nlogin_time:{}\n".format(self.name,self.surname,self.login_time)

class car_park():

    def __init__(self):

        self.connecting() 

    def connecting(self):
        self.con = sqlite3.connect("car_park_data.db") 
        self.cursor = self.con.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars (Name TEXT,Surname TEXT,Plaque ,Check_in_time timestamp)")
        
        self.con.commit()

    def disconnect(self):
        self.con.close()

    def show_records(self): 
        self.cursor.execute("Select * From cars")
      
        list1 = self.cursor.fetchall()
     
        if(len(list1) == 0):
            return "There are no cars in the parking lot"
        else:
            for i in list1:
                print(i)
            return None


    def show_customer(self,name,surname):

        self.cursor.execute("Select *From cars where Name = ? ",(name,)) 
        list2= self.cursor.fetchall()
        if (len(list2) == 0):
            print("There is no such customer record")
            return "There is no such customer record"

        else:

            print("...customer registration...\n")

            for i in list2:
                if (i[0] == name and i[1] == surname):
                    print(i)
                    print("\n")
                    return i

    def car_named(self,name,surname,number_plate):  


        self.cursor.execute("INSERT INTO cars  VALUES(?,?,?,?)",(name,surname,number_plate,datetime.now()))

        self.con.commit()

    def delete_record(self,number_plate):#sil
        k = input("{} The vehicle with number_plate will be deleted. Are you sure? Press 'Y' or 'N'".format(number_plate))
        if k == "Y":
            self.cursor.execute("Delete From cars where Plaque = ?", (number_plate,))
            self.con.commit()
            print("Recording is being deleted...")
            time.sleep(1)
            print("Record successfully deleted.")




    def update(self,name,surname,number_plate):
        while True:
            if(self.show_customer(name,surname) == "There are no cars in the parking lot"):
                break


            b = input("""What information of the customer do you want to update?
                   1.name surname
                   2.number_plate
                   You cannot make any other updates. The customer's date information starts from the moment they log in to the system.""")

            if(b == "1"):
                new_name = input("Enter new name:")
                new_surname = input("Enter your new surname:")
                self.cursor.execute("Update cars set Name = ? where Name = ?", (new_name, name))
                self.cursor.execute("Update cars set Surname = ? where Surname = ?", (new_surname, surname))
                self.con.commit()
                time.sleep(2)
                print("Customer information updated successfully")
                break


            elif(b == "2"):
                new_plaque = input("Enter the new number_plate:")
                self.cursor.execute("Update cars set Plaque = ? where Plaque = ?", (new_plaque,number_plate))
                self.con.commit()
                print("Customer information updated successfully")
                break

            else:

                print("Please enter a valid transaction")

    def search_plaque(self,number_plate):
        self.cursor.execute("Select * From cars where Plaque = ?",(number_plate,))
        list4 = self.cursor.fetchall()
        print(list4)
        login = list4[0][3]
        return login


    def log_out(self,number_plate):
        one_hour_fee = 30
        one_minute_fee = 0.5
        login = self.search_plaque(number_plate)
        login.split(" ")
        login = list(login)
        end = datetime.now()
        end = str(end)
        end = list(end)
        list1 = list(login[11:19])
        list2 = list(end[11:19])
        a= " "
        b= " "

        for i in list1:
            if( i == ":" ):

                continue
            a += str(i)

        for i in list2:
            if(i == ":"):

                continue
            b += str(i)

        if(int(a) > int(b)):
            hour = int(a) - int(b)

        elif(int(a) < int(b)):
            hour = int(b) - int(a)

       
        hour = str(hour)
        hour = list(hour)


        price = (int(hour[0]) * one_hour_fee) + (int(hour [1]) * one_minute_fee)

        print( "The amount you have to pay {} TL".format(price))

        self.delete_record(number_plate)
        time.sleep(1)
        print("Customer exited...")




# In[2]:


print("""
Welcome to Our Parking Lot System;

1. Show parking status

2.Search for customers

3. Add Record

4.Deregister

5. Update Record

6. Calculate Car Exit and Fare

Press "q" to exit""")

car_park1 = car_park()

while True:
    s = input("\nEnter your choice:")
    if(s == "q"):
        print("Process terminated.")
        break

    elif(s == "1"):
        car_park1.show_records()

    elif (s == "2"):
        name = input("Enter the name of the customer to be searched:")
        surname = input("Enter your surname:")
        car_park1.show_customer(name,surname)


    elif (s == "3"):
        name = input("Enter the name of the customer to be added:")
        surname = input("Enter your surname:")
        number_plate = input("Enter number_plate:")
        car_park1.car_named(name,surname,number_plate)
        print("\nAdding customer...")
        time.sleep(2)
        print("Customer added.")


    elif (s == "4"):
        number_plate = input("Enter the number_plate of the car to be deleted:")

        car_park1.delete_record(number_plate)


    elif (s== "5"):
        name = input("Enter the name of the customer whose information will be updated:")
        surname = input("enter your surname:")
        number_plate = input("enter number_plate:")
        car_park1.update(name,surname,number_plate)

    elif (s == "6"):
        number_plate = input("Enter the number_plate of the car for which you want to know the parking fee:")
        car_park1.log_out(number_plate)

    else:
        print("Please enter a valid transaction")


# In[ ]:




