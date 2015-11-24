__author__ = 'Dean, Abel'
import socket
from producer_thread import Producer
from Queue import Queue
global dictionary_food
dictionary_food={}



def user_main():
    try:
        addr= ("192.168.1.141", 5002)
        sock = socket.socket()
        sock.bind(addr)
        sock.listen(1)
        print "Waiting for connection..."
        client,client_addr = sock.accept()
        print "Made connection with client --->",client_addr
        user_info_in = client.recv(1024)
        print "Received:", user_info_in
        user_info_list = user_info_in.split(' ')
        print user_info_list
        client.send("received")
    finally:
        "Closing socket..."
        sock.close()
        client.close()
        return user_info_list

def setup_bf(bf_size):
    list = ["apple","rice","banana"]
    global dictionary_food
    # print "1:",dictionary_food

    for i in list:
        # dictionary_food.update({i:Queue(maxsize=bf_size)})
        # a =Queue(maxsize=bf_size)
        # a.put(10)
        # dictionary_food[i]=a
        dictionary_food[i]= Queue(maxsize=bf_size)

    # print "2:",dictionary_food




def setup(user_info):
    if len(user_info) == 2:
        num_producers = int(user_info[0])
        setup_bf(int(user_info[1]))
        for i in xrange(0, num_producers):
            Producer(name="Producer_{}".format(i+1)).start()
            # print(i)
    else:
        print("System exit... Incorrect data")
        exit(0)

if __name__ == '__main__':
    # global dictionary_food

    # setup(user_main())


    # setup([10, 10])
    # setup([10, 10, 1])
    print "0:",dictionary_food
    setup_bf(3)
    print "3:",dictionary_food
    print "len->",len(dictionary_food)
    dictionary_food["apple"].put(5)
    for i in dictionary_food.values():
        print i.qsize()





