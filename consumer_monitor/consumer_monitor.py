__author__ = 'Dean, Abel'
import socket
from random import choice
from threading import Thread,RLock
from time import sleep
import sys
lock = RLock()


def main():
    # consumer_num = raw_input("How many consumers do you want?")
    # producer_num = raw_input("How many producers do you want to produce?")
    # buffer_size = raw_input("What is the size of the buffer you want to restrict the producers to produce?")
    consumer_num = 2500
    producer_num = 500
    buffer_size = 500

    # s = socket.socket()
    # s.connect(("192.168.1.141",5002))#request a connection with the listening server
    # list= "%s %s"%(producer_num,buffer_size)
    # s.send(list)
    # # print "!!!!!!Waiting to receive 'Ready'!!!!!!!!!"
    # # data = s.recv(1024)
    # # if not data:
    try:
        s = socket.socket()
        # s.connect(("192.168.1.141",5002))#request a connection with the listening server
        s.connect(("192.168.1.193",5002))#request a connection with the listening server
        str_of_list= "%s %s"%(producer_num,buffer_size)
        s.send(str_of_list)
        data = s.recv(1024)
        if data != "Ready...":
            print "Error happened"
            s.close()
            exit(0)
            # raise SystemExit
    except socket.error as error:
        print "{"+str(error)+"}","Wasn't able to send 'Done' because lost connection"
        s.close()
        exit(0)
    # finally:
    print "!!CLOSING!!"
    s.close()
    return consumer_num


def client_socket(food,recipe_list,c_n):
    '''

    :param x: client name changing
    :param c_n: client name
    :return:
    '''
    # buffer_server = ("192.168.1.141",5007)
    buffer_server = ("192.168.1.193",5007)

    s = socket.socket()
    counter = 0
    while True:
        try:
            s.connect(buffer_server)#request a connection with the listening server
            break
        except socket.error as error:
            print "Attempting to reconnect"
            s.close()
            s=socket.socket()
            counter +=1
    # print c_n,"Connected to:->",buffer_server
    # print c_n,"Sending:->",str_list
    if counter == 4:
        print "!"*1000
    #Mabey put try catch arround all of this TODO
    print c_n,"Food:->",food,": Recipe_list:->",recipe_list
    for i in recipe_list:
        lock.acquire()
        print c_n,"Sending:->",i
        lock.release()
        s.send(i)

        ####
        # CAREFUL COULD HAVE TO DO SOME TYPE OF WAITING TO MAKE SURE THE TCP CONNECTION DOESNT CLOSE BECAUSE ITS WAITING
        # ON A PRODUCER TO PRODUCE SOMETHING INTO THE QUEUE. IT MIGHT BE TOO LONG.
        ####
        picture = s.recv(1024)
        if not picture:
            # print c_n, "Stopped receiving....."
            continue
        else:
            update_gui(picture)#finish it later TODO!!!
            lock.acquire()
            print "<<<<",c_n, "Received:->",picture
            lock.release()
    try:
        print ">>>>",c_n,"Sending:->'Done'"
        s.send("Done")        # print c_n,"Received:->",received
        s.close()
    except socket.error as error:
        print "{"+error+"}","Wasn't able to send 'Done' because lost connection"


def update_gui(ingredient):
    pass

def create_recipe_dictionary():
    # goodies_dictionary = {"Banana Bread": ["Banana", "Bread"],
    #                       "Apple Bread": ["Apple", "Bread"]} #"Bread", "Apple", "Banana"
    goodies_dictionary = {
    "Banana Bread":["Salt","Flour","Eggs","Sugar","Banana","Baking Soda","Butter","Yeast","Water"],
    "Apple Bread":["Salt","Flour","Eggs","Sugar","Apple","Baking Soda","Butter","Yeast","Water"],
    "Raisin Bread":["Salt","Flour","Eggs","Sugar","Raisin","Baking Soda","Butter","Yeast","Water"],
    "Pumpkin Bread":["Salt","Flour","Eggs","Sugar","Pumpkin","Baking Soda","Butter","Yeast","Water"],
    "Wheat Bread":["Salt","Eggs","Sugar","Wheat Flour","Baking Soda","Butter","Yeast","Water"],
    "Honey Bread":["Salt","Flour","Eggs","Sugar","Honey","Baking Soda","Butter","Yeast","Water"],
    "Chocolate Chip Bread":["Salt","Flour","Eggs","Sugar","Chocolate Chips","Baking Soda","Butter","Yeast","Water"],
    "Cinnamon Bread":["Salt","Flour","Eggs","Sugar","Cinnamon","Baking Soda","Butter","Yeast","Water"],
    "Pizza":["Salt","Flour","Eggs","Yeast","Water","Oil","Pepperoni","Sauce","Cheese"],
    "Mac and Cheese":["Cheese","Milk","Noodles","Water"],
    "Cheese burger":["Cheese","Hamburger","Lettuce"],
    "Spaghetti":["Cheese","Noodles","Hamburger","Sauce"]}
    return goodies_dictionary


def get_food_and_recipe(goodies):
    food = choice(goodies.keys())
    recipe_list = goodies[food]
    return food, recipe_list


def consumers(consumer_num):
    food, recipe = get_food_and_recipe(create_recipe_dictionary())
    print "Going to make",consumer_num,"Consumers++++++++++++++"
    id = 0
    # try:
    for i in xrange(int(consumer_num)):
        # Thread(target=client_socket, args=(x,"Client_{}".format(x))).start()
        try:
            Thread(target=client_socket, args=(food,recipe,"Client_{}".format(id))).start()
            # sleep(.01)
        except Exception as e:
            print "Exception:",e
            print "Too many clients and producers combined to handle."
            print "Stopping at client:",id
            break
        id += 1
    print "{{{{{Finishing making",consumer_num,"Consumers}}}}}"
    # except Exception:
    #     print "Trying to to m"
    #     exit(1)

if __name__ == '__main__':
    consumers(main())

    # consumers(10)

    # food, recipe = get_food_and_recipe(create_recipe_dictionary())
    # print food
    # print recipe
