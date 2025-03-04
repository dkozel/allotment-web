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

A virtual environment keeps dependencies managed and lets us use a specific Python version. The actual version doesn't matter, just keeping my environments consistent.
```
python3.12 -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

NodeJS was too out of date on my server to work with Prisma so `nodeenv` lets us fetch a newer version into the virtual environment. It modifies the environment so reload it.
```
python -m pip install nodeenv
nodenv -p
deactivate
source ./venv/bin/activate
```

Prisma needs to generate a some files based on the schema before first use, then the app can be launched.
```
python -m prisma generate --schema prisma.schema
python -m flask --app app run --host 127.0.0.1 --port 8080
```

### Running in "production"

[Nginx](https://nginx.org/) is to provide a TLS layer and proxy to gunicorn as the WSGI server. Configuration file: [`allotment.derekozel.com`](backend/allotment.derekkozel.com).

```
sudo cp backend/allotment-web.site /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/allotment-web.site /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

[Certbot](https://certbot.eff.org/pages/about) is used to obtain and renew the TLS certificates. Install as per EFF's [guide](https://certbot.eff.org/instructions). Here's some helpful commands to check the status, setup the certbot to work alongside the Nginx server, and check renewals work.

```
sudo certbot certificates
sudo certbot certonly --webroot -w /var/www/certbot -d nexus.derekkozel.com
sudo systemctl list-timers
sudo certbot renew --dry-run
```

A systemd service is used to run the [gunicorn](https://gunicorn.org/) server. Configuration file: [`allotment-web.service`](backend/allotment-web.service)

```
sudo cp backend/allotment-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable allotment-web
sudo systemctl start allotment-web
sudo journalctl -u allotment-web -f
```