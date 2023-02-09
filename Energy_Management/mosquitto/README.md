# mosquitto mqtt broker

### preparing and running mosquitto container
1. cd into this directory

2. run setup.sh (will eventually run docker-compose up -d)

## handy commands for configuring mosquitto
* read more about the mosquitto.conf here: https://mosquitto.org/man/mosquitto-conf-5.html
Start services
```
docker-compose up -d
```

start only mosquitto
```
docker-compose up -d mqtt_mosquitto
```

add user and password for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -b /mosquitto/config/password.txt <user> <password>
```

delete user for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -D /mosquitto/config/password.txt <username>
```

## example publishing a message with the mosquitto_pub command
```
mosquitto_pub  --host 127.0.0.1 --username "myuser" --pw "mypassword" --retain --debug --qos 1 --topic "mytopic" --message "this is my message"
```

## example subscribing to topic with the mosquitto_sub command
```
mosquitto_sub --host 127.0.0.1 --username "myuser" --pw "mypassword" --topic "mytopic"
```

## about mqtt messages
* when mqtt client publishs a message, 3 things must be included:
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

## about wills
when client connects to broker, it may inform that it has a "will"
the will is a message that it wants the broker to send when client disconnects unexpectedly

## debugging
for subscribing to everything
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "#"
```

the mqtt broker reports health status, read these by subscribing to the sys topics
```
mosquitto_sub --host <host> --username <user> --pw <pw> --topic "$SYS/#"
```
