# **KAFKA APPLICATION WITH DISPLAY PRICE AND GRAPHIC OF CRYPTOCURRENCIES**

<br>

### Programming in python 3.8.3 

## Available streams
***
+  All APIs have been retrieved from CoinGecko

   https://www.coingecko.com/en/api#explore-api
   
+  And we mainly used the following API to adjust the parameters according to the user's requests

   https://api.coingecko.com/api/v3/coins/"name_cryptocurrency"

## Available topics
***
+  *bitcoin* : bitcoin data (btc)
+  *ethereum* : ethereum data (eth)
+  *polkadot* : polkadot data (dot)
+  *link* : link data (lnk)
+  *havven* : havven data (snx)
+  *cardano* : average air quality index on a 30 minutes window (ada)
+  *listCoin* : data of all cryptocurrencies of current price in euros

## Running the application
***

+  To launch the application, run docker-compose up in the following path
	-->	./Kafka_Docker/src/main/docker-compose.yml

+  You need to run the [Kafka producer](./producer.py) to request datas from Api and stock in the broker Kafka with the following command 
	--> python3.8 producer.py

+ It is recommended to let the producer run for 5 to 10 minutes to obtain interesting data. (the time of loading and changing the price of the coins) 

+  To display the price or graphic of the cryptocurrencies you have to run [Kafka consumer](./consumer.py) with the following command 
	--> python3.8 consumer.py

+ You will see a menu allowing you to test the different functionalities of the application.

+  The UI is accessible on *192.168.99.100:3030* or *localhost:3030*. Depends on your configuration.


# Good experimentation ! 