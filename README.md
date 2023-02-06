# Summary

To build an e-commerce website to facilitate the selling of apparel for a small business. 
The website’s search will be powered by the Unbxd API and handle about 50 requests per second. 
The website will feature various products organized by categories and subcategories to ensure that the customers are able to find the right product. 
Frontend - React, Backend - Flask, Database - PostgreSQL, Redis, Hosted - Docker

# API Specs 

The app works on 4 main APIs:

## 1. Insert API - 
This is a POST request. The request sends a single JSON object in its body to be stores in the PostgreSql database.

POST /insert HTTP/1.1
HOST: aboutthefit
Content_type: application/json
Content_length: __Size of json file__
{
//sample data
"categoryType": "Shirts",
"productDescription": "Our performance dress shirt is easy care, so that you can look sharp with little effort. Wear this shirt from work days to weekends with chinos or jeans.",
 "title": "slim button-down wrinkle resistant performance dress shirt",
 ...
 "name": "slim button-down wrinkle resistant performance dress shirt"
}


## 2. Category API -
This is a GET request. The API retrieves category name(s) from the URL path. The parameters of the request contains sort option and page number. The response contains the first 10 json objects of the products that satisfy the conditions specified. It also contains the page number, number of pages, number of products.

GET /category/<catlevel1Name>/<catlevel2Name>/?sort=* &page=* HTTP/1.1
HOST: aboutthefit

## 3. Search API -
This is a GET request. The request parameters contain the search query, sort options and page number. The API formats and sends this request to the UNBXD API as another GET request. The API again formats the UNBXD APIs response and send it as a response. The response contains a list of json objects of the products that match the search query and other specified conditions. It also contains the page number, number of pages, number of products.

GET /search?q=* &sort=* &page=* HTTP/1.1
HOST: aboutthefit

## 4. Product API -
This is a GET request. The API retrieves "sku" from the URL path. There are no additional parameters. The response object contains the json object of the product matching the given sku.

GET /product/<sku> HTTP/1.1
HOST: aboutthefit

## Link to Postman collection -
https://api.postman.com/collections/25321732-a00f5646-5f11-4664-a43d-5b2d6461cb24?access_key=PMAT-01GRJSJEDW1K16J2T9V3PPRRHB

# Docker Installation Instruction

1. Install and open Docker Desktop
2. Within the "aboutthefit" folder, run the command - "docker compose up -d --build" to build the docker images

# Running the Services

1. Run the command "docker compose up" in the "aboutthefit" folder to run the container
2. Initially, to push the data from the json file into the database run the command "docker exec -it aboutthefit python3 json_to_db_pipeline.py"

