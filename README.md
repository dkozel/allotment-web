# How's the Allotment?

The goal of this project is an elegant and minimalistic dashboard showing the recent environment from the allotment. WeatherSpark's [temperature plot](https://weatherspark.com/h/y/37834/2025/Historical-Weather-during-2025-in-Cardiff-United-Kingdom#Figures-Temperature) is the design inspiration, providing clear data viewing and browsing of the info by [day](https://weatherspark.com/h/d/37834/2024/6/26/Historical-Weather-on-Wednesday-June-26-2024-in-Cardiff-United-Kingdom#Figures-Temperature), [month](https://weatherspark.com/h/m/37834/2024/6/Historical-Weather-in-June-2024-in-Cardiff-United-Kingdom#Figures-Temperature), and [year](https://weatherspark.com/h/y/37834/2024/Historical-Weather-during-2024-in-Cardiff-United-Kingdom#Figures-Temperature).

## Sensors

Two Dragino LHT65N LoRa sensors ([manual](https://wiki.dragino.com/xwiki/bin/view/Main/User%20Manual%20for%20LoRaWAN%20End%20Nodes/LHT65N%20LoRaWAN%20Temperature%20%26%20Humidity%20Sensor%20Manual/#H4.13AutoSendNone-ACKmessages)) are collecting temperature and humidity data.

Shed:
 * Air temperature
 * Air humidity
 * Outdoor air temperature

Greenhouse
 * Air temperature
 * Air humidity
 * Soil temperature

The data is received by The Things Stack public LoRaWAN network which calls a [webhook](https://www.thethingsindustries.com/docs/integrations/webhooks/) in this application each time a measurement is successfully uplinked.

## Saving the Measurements

A Flask application exposes an endpoint at `/tts/uplink/message` which receives a JSON payload for each measurement.

Prisma is used to manage the storing and retrieving of measurements in a SQLite database.

## Viewing the Data

A React application retrieves and renders the data into plots, creating the dashboard.

# Setup

```
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

```
python -m pip install nodeenv
nodenv -p
deactivate
source ./venv/bin/activate
```

```
python -m prisma generate --schema prisma.schema
python -m flask --app app run --host nexus.derekkozel.com
```