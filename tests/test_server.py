
# How to create and connect to posgres on Github Actions
# https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers
import requests
import random

sample_data = {
    "color": [
        "White"
    ],
    "categoryType": "Shirts",
    "productUrl": "/clothing/men/slim-button-down-wrinkle-resistant-performance-dress-shirt/pro/01705319/cat2560003",
    "availability": "true",
    "size": [
        "XL",
        "M",
        "L",
        "L Tall",
        "XXL Tall",
        "S",
        "M Tall",
        "XL Tall",
        "XS",
        "XXL"
    ],
    "category": [
        "New Arrivals",
        "*M INCLUSION - MARCH DM (40% Off any shirt or top) - 12.27",
        "Performance Dress Shirts",
        "Slim Fit Dress Shirts",
        "1MX & Patterned Dress Shirts",
        "Tops",
        "Shirt Shop"
    ],
    "productDescription": "Our performance dress shirt is easy care, so that you can look sharp with little effort. Wear this shirt from work days to weekends with chinos or jeans.",
    "catlevel2Name": "New Arrivals",
    "title": "slim button-down wrinkle resistant performance dress shirt",
    "productImage": "https://images.express.com/is/image/expressfashion/0020_01705319_0001?cache=on&wid=361&fmt=jpeg&qlt=75,1&resmode=sharp2&op_usm=1,1,5,0&defaultImage=Photo-Coming-Soon",
    "sku": str(random.randint(10000000, 99999999)),
    "price": 59.9,
    "catlevel3Name": "New Arrivals",
    "catlevel1Name": "men",
    "name": "slim button-down wrinkle resistant performance dress shirt",
    "gender": [
        "men"
    ],
    "catlevel4Name": "Performance Dress Shirts",
    "uniqueId": "01705319"
    }

def test_server_check():
    assert True, "Server not up"

def test_hosted():

    response = requests.get("http://[::1]:5000/check")
    assert response.status_code == 200, "Server not up"

def test_insert():

    response = requests.post("http://[::1]:5000/insert", json=sample_data)
    assert response.status_code == 200, "Insertion failed"
