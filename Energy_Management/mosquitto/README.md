## mosquitto - the mqtt broker

### documentation and man pages 
* [mosquitto](https://mosquitto.org/man/mosquitto-8.html)
* [mosquitto_pub](https://mosquitto.org/man/mosquitto_pub-1.html)
* [mosquitto_sub](https://mosquitto.org/man/mosquitto_sub-1.html)
* [MQTT](https://mosquitto.org/man/mqtt-7.html)
* [mosquitto man page home](https://mosquitto.org/man/)

## Setup
1. cd into this directory
2. run setup.sh

## handy commands for configuring mosquitto
* read more about the mosquitto.conf here: https://mosquitto.org/man/mosquitto-conf-5.html

### Start services (as daemon, or omit "-d" for log output)
```
docker-compose up -d
```

### start only mosquitto
```
docker-compose up -d mqtt_mosquitto
```

### add user and password for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -b /mosquitto/config/password.txt <user> <password>
```

### delete user for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -D /mosquitto/config/password.txt <username>
```

### mosquitto_pub example: publish a message with the mosquitto_pub command
```
mosquitto_pub  --host 127.0.0.1 --username "myuser" --pw "mypassword" --retain --debug --qos 1 --topic "mytopic" --message "this is my message"
```

### mosquitto_sub example: subscribe to a topic with the mosquitto_sub command
```
mosquitto_sub --host 127.0.0.1 --username "myuser" --pw "mypassword" --topic "mytopic"
```

## debugging
### for subscribing to everything
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "#"
```

### the mqtt broker reports convenient info in the $SYS topic
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "$SYS/#"
```

### get number of persisted messages
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "$SYS/broker/store/messages/count"
```

### get number of persisted bytes
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "$SYS/broker/store/messages/bytes"
```

### read latest log output (provided the log-path /mosquitto/log/mosquitto.log)
```
tail /mosquitto/log/mosquitto.log
```

## MQTT design
### 3 things must be included when a client publishes a message:
1. Topic
  - used to filter messages so each one is only delivered to recipients it concerns
  - only ASCII characters
  - use subtopics (the use of a single topic for sending messages are discuraged)
  - subtopics can have many/multiple layers
  - example for subtopic if having different types of sensors in the same room that publishs data
    - building2/floor1/roomA/temperature
    - building2/floor1/roomA/brightness
    - building2/floor1/roomA/humidity
  - wildcards for subscribing to multiple topics uses "+" for single level and "#" all remaining levels
  - example for "+":
    - building2/+/roomA/humidity
    - +/floor1/+/temperature
  - example for "#":
    - building2/#
    - building2/floor1/#
  - example using both:
    - building2/+/roomA/#

2. Quality of Service level
  - QoS level 0 (at most once)
    - no guarantee of delivery
    - provides the same guarantee as the underlying TCP protocol
    - recipient does not acknowledge receipt of the message
    - the message is not stored and re-transmitted by the sender
    - often called "fire and forget"
    - does not store messages queues for if subscriber client if off-line
    - use when loss of some messages can be acceptable or data not that important or sent in short intervals
  - QoS level 1 (at least once)
    - guarantees that a message is delivered at least one time to the receiver
    - possible for a message to be sent or delivered multiple times
    - most frequently used
    - stores messages queues for when subscriber client is off-line
    - use when every message needs to be received, but can handle duplicates
  - QoS level 2 (exactly once and most overhead)
    - guarantees that each message is received only once by the intended recipients
    - guarantee is provided by at least two request/response flows (a four-part handshake) between sender and receiver
    - use when it is critical that your application receives all messages exactly once
    - stores messages queues for when subscriber client is off-line

3. Retain Flag (if issued then it will be set to True)
  - mqtt broker will keep the message even after sending it to all current subscribers
  - if subscription from a new client is made, the message will be sent to that client
  - use when subscribed client cannot wait until next message is published

### wills (when client disconnects)
when client connects to broker, it may inform that it has a "will"
the will is a message that it wants the broker to send when client disconnects unexpectedly

### clean sessions (durable/non-durable clients)
when to use
  - used if client only publish messages
  - used for none durable clients
  - broker does not store undelivered messages
  - broker does not store client information (client id etc.)
when to not use
  - for durable cients
  - used if client must receive (almost) all messages
  - clients using QoS level 1 or 2 will get stored messages from brker
  - broker keeps undelivered messages (delivered messages are still removed)
