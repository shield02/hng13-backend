# STAGE 2 TASK - Country Currency & Exchange API

A RESTful API that fetches country data from an 
external API, stores it in a database, and provides CRUD operations.

### Functionalities

Fetch country data from: `https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies`

For each country, extract the currency code (e.g. NGN, USD, GBP).

Then fetch the exchange rate from: `https://open.er-api.com/v6/latest/USD`

Match each country's currency with its rate (e.g. NGN → 1600).

Compute a field estimated_gdp = population × random(1000–2000) ÷ exchange_rate.

Store or update everything in MySQL as cached data.

### Endpoints

POST `/countries/refresh` → Fetch all countries and exchange rates, then cache them in the database

GET `/countries `→ Get all countries from the DB (support filters and sorting) - ?region=Africa | ?currency=NGN | ?sort=gdp_desc

GET `/countries/:name` → Get one country by name

DELETE `/countries/:name` → Delete a country record

GET `/status` → Show total countries and last refresh timestamp

GET `/countries/image` → serve summary image

## How to Run the App Locally

`make up`: start and builder the containers

`make down`:  stop containers

`make restart`: stop and start containers

`make refresh`: refresh the database (pull all data and populate DB)

`make status`: check status

`make countries`: fetch all countries

`make country`: fetch data for a country --usage `make country COUNTRY=Nigeria`

`make delete`: delete a country --usage `make delete COUNTRY=Nigeria`

`make image`: fetch the image

`make clear-chace`: clear the cache image