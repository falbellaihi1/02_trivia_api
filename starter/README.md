# Trivia API 

#INTRODUCTION 
This udacity project Trivial API 
Udacity is invested in creating bonding experiences for its employees and students. 
A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, 
but their API experience is limited and still needs to be built out.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql


```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:


```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

or windows 
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

```




Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).
#### Installing project 
 run 

```bash
npm install
```




- navigate to project directory and to starter>frontend using CMD/BASH
```
npm start
```


-BASE URL 
    - Backend URL
    
        
        http://127.0.0.1:5000/
   -frontend URL
   
        ```http://127.0.0.1:3000/```
        
        






#HTTP STATUS CODE SUMMARY AND FORMAT
- 200 OK

    * Everything is working as it should



- 404 resource not found

example

``` quizzes?category=4``` (none existent category)


Returns
   ``` {
      "error": 404,
      "message": "resource not found",
      "success": false
    }
```
 - 422 unprocessable
 
    * POST \questions   


    
        { // JSON
            "question" :""
         }
   
- returns 
   
```
    {
      "error": 422,
      "message": "unprocessable",
      "success": false
    }
```
- 405 method not allowed
        {
            "error": 405,
            "message":method not allowed,
            "success": False,
        }
       
           
            
- 500 Internal Server Error
        
        {
            "error": 500,
            "message":Internal Server Error,
            "success": False,
        }  







```

API DOCUMENTATION
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...
```




#Categories
GET '/categories'
-General
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

-To get categories
    * ```curl --location --request GET 'http://127.0.0.1:5000/categories' ```
```{
  "categories": {
    "1": "entertainment",
    "2": "history"
  },
  "success": true,
  "total_categories": 2
}
```



GET ```'/categories/<int:category_id>/questions```
- General
    - Returns all questions in passed category id
    - Request Arguments: category id
 - ```curl --location --request GET http://127.0.0.1:5000/categories/2/questions ```
    - Returns:

```{
  "current_category": "history",
  "questions": [
    {
      "answer": "Real Madrid",
      "category": "1",
      "difficulty": 1,
      "id": 31,
      "question": "In football, which team has won the Champions League (formerly the European Cup) the most?"
    },
    
    {
      "answer": "George Washington",
      "category": "1",
      "difficulty": 1,
      "id": 32,
      "question": "Who is the first president of the United States of America?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#Questions
GET '/questions'
- General
    - Fetches a dictionary of all qustions in which the key is current category and question key, the question key contains keys: (category, answer, difficulty, id) and the value is the corresponding string of the keys
    - For paginated
        * ```curl --location --request GET 'http://127.0.0.1:5000/questions?page=1' ```
    - for all
        * ```curl --location --request GET 'http://127.0.0.1:5000/questions' ```

- returns questions in first page (10 questions per page)
```{
  "categories": {
    "1": "entertainment",
    "2": "history"
  },
  "current_category": "history",
  "questions": [
    {
      "answer": "Catherine Parr",
      "category": "2",
      "difficulty": 5,
      "id": 26,
      "question": "Who was Henry VIIIs last wife"
    },
    {
      "answer": "1431",
      "category": "2",
      "difficulty": 5,
      "id": 27,
      "question": "In which year was Joan of Arc burned at the stake?"
    },

    {
      "answer": "Real Madrid",
      "category": "1",
      "difficulty": 1,
      "id": 31,
      "question": "In football, which team has won the Champions League (formerly the European Cup) the most?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

DELETE '/questions/<int:question_id>'
General
    - Deletes question with passed id
    - Request Arguments: question id
    - Deleting question 
    
   * ``` curl --location --request DELETE 'http://127.0.0.1:5000/questions/26' ```
- Returns:. 
```{
  "success": true,
  "created": 90
}
```

POST '/questions
-General
    - Creates question 
    - Request Arguments: question, answer, difficulty, category
```
curl --location --request POST 'http://127.0.0.1:5000/questions' \
--header 'Content-Type: application/json' \
--data-raw '{
             "question" :"Who is the first president of the United States of Great America?",
             "answer": "George Washington",
             "difficulty": 1,
             "category": "1"

        }'
```
- Returns:. 
```{
  "created": 32,
  "success": true
}
```

POST '/questions/search
- General
    - searches questions for given search term 
    - Request Arguments: searchTerm
```curl --location --request POST 'http://127.0.0.1:5000/questions/search' \
--header 'Content-Type: application/json' \
--data-raw '{"searchTerm":"who"} ```

- Returns:. 
```{
  "current_category": "history",
  "questions": [
    {
      "answer": "Catherine Parr",
      "category": "2",
      "difficulty": 5,
      "id": 26,
      "question": "Who was Henry VIIIs last wife"
    },
    
    {
      "answer": "USA",
      "category": "2",
      "difficulty": 3,
      "id": 29,
      "question": "Who won the FIFA Women's World Cup in 2019?"
    },
    {
      "answer": "George Washington",
      "category": "1",
      "difficulty": 1,
      "id": 32,
      "question": "Who is the first president of the United States of America?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#Quiz

POST '/quizzes'
- General
    - Returns random question in choosen category
    - Request Arguments: category id
    - Can play quiz in all categories by passing category id of '0'
 ```
   curl --location --request POST 'http://127.0.0.1:5000/quizzes?category=1' \
--header 'Content-Type: application/json' \
--data-raw '{"previous_questions": [0]}'
``` 

- returns random questions in category id 1
 
```
   curl --location --request POST 'http://127.0.0.1:5000/quizzes?category=1' \
--header 'Content-Type: application/json' \
--data-raw '{"previous_questions": [0]}'
``` 
- returns random question from all questions in all categories 


- example return of ```/quizzes?category=1```
```{
  "question": {
    "answer": "George Washington",
    "category": "1",
    "difficulty": 1,
    "id": 32,
    "question": "Who is the first president of the United States of America?"
  },
  "success": true
}
```

              


##Authors


#Achnowledgements
Team of Udacity
