![pylint workflow](https://github.com/unbxd-internship/abouthefit/actions/workflows/pylint.yml/badge.svg)
![pytest workflow](https://github.com/unbxd-internship/abouthefit/actions/workflows/pytest.yml/badge.svg)
# Summary

To build an e-commerce website to facilitate the selling of apparel for a small business.
The website’s search will be powered by the Unbxd API and handle about 50 requests per second.
The website will feature various products organized by categories and subcategories to ensure that the customers are able to find the right product.
Frontend - React, Backend - Flask, Database - PostgreSQL, Redis, Hosted - Docker

<hr/>
# API Specs

The app works on 4 main APIs:

## 1. Insert API -
This is a POST request. The request sends a single JSON object in its body to be stores in the PostgreSql database.

```
POST /insert HTTP/1.1
HOST: aboutthefit.as
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
```

## 2. CategoryHeader API - 
This is a GET request. The API retrieves category headers from the database. The response contains a dictionary, with a list of cat-1 headers and corresponding cat-2 headers as values.

```
GET /category_headers HTTP/1.1
HOST: aboutthefit.as
```

## 3. Category API -
This is a GET request. The API retrieves category name(s) from the URL path. The parameters of the request contains sort option and page number. The response contains the first 10 json objects of the products that satisfy the conditions specified. It also contains the page number, number of pages, number of products.

```
GET /category/(catlevel1Name)/(catlevel2Name)/?sort=* &page=* HTTP/1.1
HOST: aboutthefit.as
```

## 4. Search API -
This is a GET request. The request parameters contain the search query, sort options and page number. The API formats and sends this request to the UNBXD API as another GET request. The API again formats the UNBXD APIs response and send it as a response. The response contains a list of json objects of the products that match the search query and other specified conditions. It also contains the page number, number of pages, number of products.

```
GET /search?q=* &sort=* &page=* HTTP/1.1
HOST: aboutthefit.as
```

## 5. Product API -
This is a GET request. The API retrieves "sku" from the URL path. There are no additional parameters. The response object contains the json object of the product matching the given sku.

```
GET /product/(sku) HTTP/1.1
HOST: aboutthefit.as
```

## 6. Recommend API - 
This is a GET request. The API retrieves "sku" from the URL path, and the response object contains 4 similar products.

```
GET /recommend/(product_id) HTTP/1.1
HOST: aboutthefit.as
```

## Link to Postman collection -
<href> https://api.postman.com/collections/25321732-a00f5646-5f11-4664-a43d-5b2d6461cb24?access_key=PMAT-01GRJSJEDW1K16J2T9V3PPRRHB <href>

<hr/>
# Docker Images

The frontend and the backend are built on separate docker images.

Command to pull the images -

## Frontend - 
`docker pull anchal31sharma/atf-frontend:v1`

## Backend -
`docker pull anchal31sharma/atf-backend:v1`

The frontend can be accessed on http://localhost:3000/
The backend can be accessed on http://localhost:5000/

## To ingest json data into the database
A file called "json_to_db_pipeline.py" has to be run within the docker container to perform ingestion. This can be done by:
`docker exec -it atf-backend python3 json_to_db_pipeline.py`

<hr/>
# Kubernetes Deployment

To deploy these docker images on a Kubernetes Kind Cluster

## 1. Create the cluster
`kind create cluster --name aboutthefit --config=/deployment/workerNodes.yaml`

## 2. Set up Ingress
```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
kubectl wait --namespace metallb-system  --for=condition=ready pod  --selector=app=metallb --timeout=90s
kubectl apply -f https://kind.sigs.k8s.io/examples/loadbalancer/metallb-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod  --selector=app.kubernetes.io/component=controller --timeout=90s
```

## 3. Apply Kubernetes Manifests
`kubectl apply -f deployment/`

## 4. Check if Ingress is enabled
`kubectl get ingress`

## 5. Add preferred HostName (as specified in ingress file)
`sudo vi /etc/hosts`
add to this file 
`127.0.0.1       aboutthefit.as`

## 6. Port Forward the Backend
`kubectl port-forward service/api 5000:5000`

## 7. To ingest json data into the database
A file called "json_to_db_pipeline.py" has to be run within the cluster to perform ingestion. This can be done by:

###   a. Checking the name of the API pod
`kubectl get pods`

###   b. Copy the pod name for api and run
`kubectl exec -it pod_name python3 json_to_db_pipeline.py`

<hr/>
Images of Functional Website





