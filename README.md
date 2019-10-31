# Yelp Recommendation System

The full stack recommendation system uses flask, HTML, CSS, JavaScript and Bootstrap4. 
The recommendation system is based on collaborative filtering algorithms. 
When searching the contents, system uses the Okapi BM25F ranking function from Whoosh library.
The project requires Python 3.7.

 
## Data
The original dataset is from [Yelp Dataset](https://www.kaggle.com/yelp-dataset/yelp-dataset). I choose some parts of data in the Las Vegas.
You should download my dataset [here](https://drive.google.com/drive/folders/1fK7sBOSdXSAXyWRCpCpLfP12G56Qg0-z?usp=sharing). It contains three json files. 
Then put all files under yelp_recommendation_system/app/res. 
To download and use data, you agree to the [Yelp Dataset Terms of Use](./yelp-dataset-agreement.pdf).



## Preprocess
You must download my dataset first. Under yelp_recommendation_system directory, run command line:
```bash
> sh preprocess.sh
```

## Usage
Launching a very simple builtin server by flask. Under yelp_recommendation_system directory, run command line:
```bash
> export FLASK_APP=app    
> export FLASK_ENV=development
> flask run
```
Open http://127.0.0.1:5000 on browser.


In the sqlite database, I already saved 6722 users. The usernames and passwords are same from 0 to 6721. 
After you login in, collaborative filtering will be used when you search restaurants. 
Although you can create new users, collaborative filtering will not be used for new users. 
After searching, you will get at most 12 top restaurants which are most relative with your query words.
 If you want to show the google map in the website, you need to change [[YOUR_API_KEY]](./app/templates/index.html#L73) in the code.
 
## Docker
The docker image is based on [uwsgi-nginx-flask-docker](https://github.com/tiangolo/uwsgi-nginx-flask-docker).

Build Flask image:
```bash
> docker build -t myimage .
```
Run a container based on image:
```bash
> docker run -d --name mycontainer -p 8080:8080 myimage
```
Open http://127.0.0.1:8080 on browser.

## License
[MIT](./LICENSE)

## Links
* [flask](https://github.com/pallets/flask)
* [flask-sqlalchemy](https://github.com/pallets/flask-sqlalchemy)
* [flask_login](https://github.com/maxcountryman/flask-login)
* [whoosh](https://whoosh.readthedocs.io/en/latest/)
* [uwsgi-nginx-flask-docker](https://github.com/tiangolo/uwsgi-nginx-flask-docker)
* [Bootstrap](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
* [Yelp Dataset](https://www.kaggle.com/yelp-dataset/yelp-dataset)
