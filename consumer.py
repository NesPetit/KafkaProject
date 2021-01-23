from kafka import KafkaConsumer
from kafka.errors import KafkaError
from tkinter import *
import tkinter.ttk
import time
import json
import requests
import msgpack
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from matplotlib.animation import FuncAnimation

# To consume latest messages and auto-commit offsets
consumer1 = KafkaConsumer('bitcoin',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

consumer2 = KafkaConsumer('ethereum',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

consumer3 = KafkaConsumer('polkadot',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')
consumer4 = KafkaConsumer('link',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

consumer5 = KafkaConsumer('havven',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

consumer6 = KafkaConsumer('cardano',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

graphConsumer = KafkaConsumer('listCoin',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')), 
                         auto_offset_reset = 'earliest')

def Tableau():
    window = Tk()
    window.title("My Application")
    window.geometry("800x600")
    window.minsize(400, 200)
    frame = Frame(window)
    
    etiquette = Label(frame, text='Prix des cryptomonnaies en euros et ses variations', font=("Courrier", 20), fg = 'black')
    etiquette.pack(pady = 8)

    tableau = tkinter.ttk.Treeview(frame, columns=('compteur','symbol', 'name', 'price', 'varia'))

    tableau.column('compteur', width=30, minwidth = 30, anchor = "center")
    tableau.column('symbol', width=80, minwidth = 80, anchor = "center")
    tableau.column('name', width=100, minwidth = 100, anchor = "center")
    tableau.column('price', width=90, minwidth = 90, anchor = "center")
    tableau.column('varia', width=100, minwidth = 100, anchor = "center")

    tableau.heading('compteur', text=' ')
    tableau.heading('symbol', text='Symbol')
    tableau.heading('name', text='Name')
    tableau.heading('price', text='Price')
    tableau.heading('varia', text='% Variation')
    tableau['show'] = 'headings'
    #Inserts
    first_value = [0,0,0,0,0,0]
    sign = [" "," "," "," "," "," "]
    calcul = [0,0,0,0,0,0]
    tableau.insert("", 1,"1", text = 1, values = (1, "BTC", "Bitcoin", "s", ""))
    tableau.insert("", 2,"2", text = 2, values = (2, "ETH", "Ethereum", "", ""))
    tableau.insert("", 3,"3", text = 3, values = (3, "DOT", "Polkadot", "", ""))
    tableau.insert("", 4,"4", text = 4, values = (4, "LNK", "Link", "", ""))
    tableau.insert("", 5,"5", text = 5, values = (5, "SNX", "Havven", "", ""))
    tableau.insert("", 6,"6", text = 6, values = (6, "ADA", "Cardano", "", ""))

    i = 0
    graphConsumer.poll()
    graphConsumer.seek_to_beginning()
    
    coins = ["btc", "eth","dot","lnk","snx", "ada"]
    for msg in graphConsumer:
        for i in range(0,5,1):
            if calcul[i] > 0:
                sign[i] = "+"
            else:
                sign[i] = " "
            if first_value[i] == 0:
                first_value[i] = msg.value[i]
            
            calcul[i] = round(100*((msg.value[i] - first_value[i]) / first_value[i]), 2)

        tableau.delete(1,2,3,4,5,6)
        tableau.insert("", 1, "1", text = 1, values = (1, "BTC", "Bitcoin", str(msg.value[0]), sign[0] + str(calcul[0]) + "%"))
        tableau.insert("", 2,"2", text = 2, values = (2, "ETH", "Ethereum", str(msg.value[1]), sign[1] + str(calcul[1]) + "%"))
        tableau.insert("", 3,"3", text = 3, values = (3, "DOT", "Polkadot", str(msg.value[2]), sign[2] + str(calcul[2]) + "%"))
        tableau.insert("", 4,"4", text = 4, values = (4, "LNK", "Link", str(msg.value[3]), sign[3] + str(calcul[3]) + "%"))
        tableau.insert("", 5,"5", text = 5, values = (5, "SNX", "Havven", str(msg.value[4]), sign[4] + str(calcul[4]) + "%"))
        tableau.insert("", 6,"6", text = 6, values = (6, "ADA", "Cardano", str(msg.value[5]), sign[5] + str(calcul[5]) + "%"))
        tableau.pack(expand=YES, fill='both')
        frame.pack(expand=YES, fill='both', padx = 10, pady = 40)

        window.update_idletasks()
        window.update()
    #window.mainloop()
#Afficher
def Graph(coin, currency):
    x_vals = []
    y_vals = []
    fig = plt.figure()
    plt.title('Cours du ' + coin + ' en fonction de ' + currency)
    plt.xlabel('Time (min)')         # Nom de la grandeur en abscisse
    plt.ylabel('Price (' + currency +')')         # Nom de la grandeur en ordonnée
    ax = fig.add_subplot(111)
    i = 0
    if coin == 'btc':
        consumer = consumer1
    elif coin == 'eth':
        consumer = consumer2
    elif coin == 'dot':
        consumer = consumer3
    elif coin == 'lnk':
        consumer = consumer4
    elif coin == 'snx':
        consumer = consumer5
    elif coin == 'ada':
        consumer = consumer6
    else:
        print('Veuillez rentrer un coin valide svp')
        return

    consumer.poll()
    consumer.seek_to_beginning()
    val = -1
    for msg in consumer:
        if msg.value[currency] != val:
            x_vals.append(i)
            print('value = ' + str(msg.value[currency]) + str(currency))
            y_vals.append(msg.value[currency])
            ax.plot(x_vals, y_vals, color='b')
            fig.canvas.draw()
            ax.set_xlim(right=i + 10)
            fig.show()
            plt.pause(0.01)
        val = msg.value[currency]
        i += 1
        
    plt.close()


def menu():
    choix = ''
    print("Menu principal")
    print("Quelle action souhaitez-vous effectuer ?")
    print("1 - Affichage d'un graphique crypto en temps reel (environ 2 minutes interval d'actualisation)")
    print("2 - Tableau des valeurs des cryptos en euros en temps reel avec sa variation depuis le lancement de l'application")
    print("3 - Quitter l'application")

    while choix != '1' and choix != '2':
        choix = input("Selection : ")
    
    if choix == '1':
        #fs = delete_topics('bitcoin', operation_timeout=30)
        # Faire le graph avec plot
        print("Veuillez choisir une crypto (BTC, ETH, DOT, LNK, SNX, ADA) :")
        choix1 = input().lower()
        print("Veuillez choisir une seconde monnaie supportée (EUR, USD, BTC, ETH) :")
        choix2 = input().lower()
        
        Graph(choix1, choix2)


    if choix == '2':
        #Faire le tableau avec tkinter
        Tableau()
    if choix == '3':
        print('Merci de votre visite !')
        time.sleep(2)
        quit()

menu()

consumer.close()
