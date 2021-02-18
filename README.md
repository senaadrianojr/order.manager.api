# Order Manager API

This is a sample python restful api build with flask. The purpose of this API is to manage orders and track their progress.

## Enviroment

Python 3.8

## Setup
```
pip install -r requirements.txt
```
## Execution
```
flask run
```
## Resourcers
Default host for local enviroment is http://localhost:5000

### Auth
Generates a token for authentication.

 - Path: {host}/salesman/login
 - Method: POST
 - Request body:
 ```
 {
	"login": "caseiramassas",
	"password": "caseiramassas#2020"
}
 ```
 - Response body:
```
{
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzYWxlc21hbiI6IkNhc2VpcmEgTWFzc2FzIiwiZG9jX2lkIjoiOTkuOTk5Ljk5OS85OTk5LTk5IiwiZXhwIjoxNjEzNjUyMzA3LjkzNDkwOX0.EmYqAaGJqToX4Ff1ztCvTKPTb7XrfGoUXT78EJBuo3w"
}
```
### Products
 Products CRUD.
 
 - Get all products
	 - Path: {host}/products
	 - Method: GET
	 - Header: 
		 ```
		 token={auth generated token}
		 ```
	- Response:
		 ```
		 {
			"content": [
					{
						"_id": "601342ed3b88d478c2bba62a",
						"description": "Massa pastel disco pequeno 400g (10cm)",
						"package": "48 x 400g",
						"retail_price": 3,
						"wholesale_price": 144.4
					}
				]
		}
		 ```
 - Create product:
	 - Path: {host}/products
	 - Method: POST
	 - Header:   
		 ```
		 token={auth generated token}
		 ```
	- Request body:
		 ```
		 {
			"description": "Massa Pizza fresca com 2 disco 400g",
			"package": "24 x 400g",
			"retail_price": 4.5,
			"wholesale_price": 90
		}
		 ```
	- Response body: HTTP STATUS 201
- Update product
	- Path: {host}/products/{product_id}
	- Method: PUT
	- Header:
		 ```
		 token={auth generated token}
		 ```
	- Request body:
		 ```
		 {
			"description": "Massa Pizza fresca com 2 disco 400g",
			"package": "24 x 400g",
			"retail_price": 4.8,
			"wholesale_price": 96
		}
		 ```
	- Response body: HTTP STATUS 203