# FastApi Stock Market Api

![](https://ei.marketwatch.com/Multimedia/2018/10/25/Photos/ZH/MW-GS396_NYSEP__20181025094453_ZH.jpg?uuid=26d851d6-d85c-11e8-a02d-ac162d7bc1f7)

## Description
Api that retrieves stock market data from [alphavantage](https://www.alphavantage.co). In this api users can sign up, get their api key and use it to retrieve data from the api, also all the user interactions are stored in a database to keep track of the user activity.

## Features
- Sign up
- Retrieve api key
- Retrieve stock market data
- user activity
- Retrieve logs from the api


## Installation
Clone the repository
```bash
git clone https://github.com/MasamioNakada/stock_market_api.git
```

Build the docker image 
```bash
docker build -t stock_market_api:latest .
```

Run the docker image
```bash
docker run -p 8000:8000 stock_market_api:latest
```

## API
Actually the api is running on a docker container, in a serverless environment, so you can use the api by sending requests to the following url: [https://stock-market-api-nla3j7erha-uc.a.run.app](https://stock-market-api-nla3j7erha-uc.a.run.app)

### Sign up [POST] [users]

**Endpoint**

```bash
https://stock-market-api-nla3j7erha-uc.a.run.app/users/create_user
```

**Body**

| Field      | Description          |
|-------------|----------------------|
| full_name   | Full name of the user |
| email       | User's email address |
| password    | User's password |

**Response 201**

| Field         | Description                  |
|---------------|------------------------------|
| access_token  | User's access token          |
| token_type    | User's token type            |
| expires_in    | Token expiration time        |

**Response 400**

| Field         | Description                  |
|---------------|------------------------------|
| detail        | Email already exists  |

**Example**

```bash
curl -X POST \
  'https://stock-market-api-nla3j7erha-uc.a.run.app/users/create_user' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "full_name":"John Doe",
  "email":"johndoe@example.com",
  "password":"password"
}'
```

### Retrieve api key [GET] [users]

**Endpoint**

```bash
https://stock-market-api-nla3j7erha-uc.a.run.app/users/get_access_token
```

**Headers**

| Field         | Description                  |
|---------------|------------------------------|
| Authorization | Basic {base64(user:password)}   |

Note that the user and password are the ones used to sign up in the api. It is a **basic authentication**.

**Response 200**

| Field         | Description                  |
|---------------|------------------------------|
| access_token  | User's access token          |
| token_type    | User's token type            |
| expires_in    | Token expiration time        |

**Response 401**

| Field         | Description                  |
|---------------|------------------------------|
| detail        | Invalid credentials  |

**Example**

```bash
curl -X GET \
  'https://stock-market-api-nla3j7erha-uc.a.run.app/users/get_access_token' \
  --header 'Authorization: Basic am9obmRvZUBleGFtcGxlLmNvbTpwYXNzd29yZA=='
```

### Retrieve stock market data [GET] [stocks]

**Endpoint**

```bash
https://stock-market-api-nla3j7erha-uc.a.run.app/stock/{symbol}
```

**Headers**

| Field         | Description                  |
|---------------|------------------------------|
| Authorization | Bearer {access_token}   |

**Params**

| Field         | Description                  |
|---------------|------------------------------|
| symbol        | Stock symbol                 |

**Response 200**

| Field         | Description                  |
|---------------|------------------------------|
| symbol        | Stock symbol                 |
| open          | Stock open price             |
| high          | Stock high price             |
| low           | Stock low price              |
| variation     | Variation between last 2 closing price values               |

**Response 401**

| Field         | Description                  |
|---------------|------------------------------|
| detail        | Invalid Token  |

**Response 401**

| Field         | Description                  |
|---------------|------------------------------|
| detail        | User not active, please verify your email  |

Note: to allow email verification, change in line 35 `active=True` to `False` at `routers/users.py`  

**Response 429**

| Field         | Description                  |
|---------------|------------------------------|
| detail        | Too many requests  |

Note: The api has a limit of 1 request per second and alphavantage api has a limit of 5 requests per minute and 500 requests per day, so if you try to make more than 1 requests per second or 5 request per minute you will get this response.


**Example**

```bash
curl -X GET \
  'https://stock-market-api-nla3j7erha-uc.a.run.appapi/stock/meta' \
  --header 'Authorization: Bearer {your_access_token}'
```

### Retrieve logs [GET] [logs]

**Endpoint**

```bash
https://stock-market-api-nla3j7erha-uc.a.run.app/logs
```

**Response 200**

Plain text file with the las 10 logs from the api.

Note: this endpoint should be protected by a Authentication, so only the admin can access it but for demo porpuses it is not protected.

**Example**

```bash
curl -X GET \
  'https://stock-market-api-nla3j7erha-uc.a.run.app/logs'
```

### User activity

The user activity is stored in a database, so you can check the user activity by accessing the database.

Note:
- The best way to store the user activity is in a structured database like a relational database, but for demo porpuses I used a NoSQL database.
