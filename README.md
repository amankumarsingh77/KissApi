
# KissApi

An unoffical Fast-Api project for kissasian.lu


## Features

- Detailed search results
- Detailed Series information
- Direct Stream Urls [Host: Vidmoly] 
- Get Latest updated series


## Run Locally

Clone the project

```bash
  git clone https://github.com/amankumarsingh77/KissApi.git
```

Go to the project directory

```bash
  cd KissApi
```

Install requirements

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python kiss.py
  (or)
  python3 kiss.py

```


## Deployment

To deploy this project run



```bash
  python kiss.py
  (or)
  python3 kiss.py
```



## API Reference

#### Get search results

```bash
  GET /api/search/${query}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string` | **Required**. Search term |

#### Get series information

```bash
  GET /api/series_info/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. id of the series |

#### Get stream url
```bash
  GET /api/stream/{series_id}/{ep_no}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `series_id`      | `string` | **Required**. id of the series |
| `ep_no`      | `string` | **Required**. episode number |

#### Get latest updated series

```bash
  GET /api/api/latest
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| -      | - | Returns the latest updated series and their episode with links |



For more information please run the project : (http://localhost:8000/docs) 


## Authors

- [@amankumarsingh77](https://www.github.com/amankumarsingh77)


## Feedback

If you have any feedback, feel free to create a issue.


## License

[MIT](https://choosealicense.com/licenses/mit/)

