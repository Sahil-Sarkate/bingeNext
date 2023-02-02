from flask import Flask, render_template, request, json
from flask_navigation import Navigation

import requests
import pickle
import pandas as pd

app = Flask(__name__)
nav = Navigation(app)


@app.route('/navpage')
def navpage():
    return render_template('navpage.html')


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=93a8bfabeddaf037b287771c8ae3e4fe&language=en-US'.format(
            movie_id))
    data = response.json()
    url = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return url


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_posters


@app.route('/info')
def info_slider():
    mv = movies_info[movies_info['title'] == name]
    i = mv.index[0]
    mv_id = movies.iloc[i].id
    posters = recommend(mv_id)

    return render_template('movie_info.html', posters=posters)


# cinderella, interstellar, zodiac, Avatar
def get_top():
    top_posters = []
    top_list = movies_info.sort_values(by='popularity', ascending=False)[0:20]
    top_names = []
    for i in range(15):
        top_names.append(top_list.iloc[i].title)

    for i in range(15):
        movie_id = top_list.iloc[i].id
        top_posters.append(fetch_poster(movie_id))

    return top_names, top_posters


def get_action():
    action_posters = []
    action_list = movies_info[movies_info['genres'] == 'Action']
    action_list = action_list.head(10)
    action_names = []
    for i in range(10):
        action_names.append(action_list.iloc[i].title)

    for i in range(10):
        movie_id = action_list.iloc[i].id
        action_posters.append(fetch_poster(movie_id))

    return action_names, action_posters


def get_romance():
    romance_posters = []
    romance_list = movies_info[movies_info['genres'] == 'Romance']
    romance_list = romance_list.head(10)
    romance_names = []
    for i in range(10):
        romance_names.append(romance_list.iloc[i].title)

    for i in range(10):
        movie_id = romance_list.iloc[i].id
        romance_posters.append(fetch_poster(movie_id))

    return romance_names, romance_posters


def get_crime():
    crime_posters = []
    crime_list = movies_info[movies_info['genres'] == 'Crime']

    crime_list = crime_list.head(10)
    crime_names = []
    for i in range(10):
        crime_names.append(crime_list.iloc[i].title)

    for i in range(10):
        movie_id = crime_list.iloc[i].id
        crime_posters.append(fetch_poster(movie_id))

    return crime_names, crime_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

info = pickle.load(open('movies.pkl', 'rb'))
movies_info = pd.DataFrame(info)

similarity = pickle.load(open('similarity.pkl', 'rb'))

m_id = 0
ind = 0
name = ''

app = Flask(__name__, template_folder='templates', static_folder="static")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome', methods =["GET", "POST"])
def index2():
    top_names, top_posters = get_top()
    action_names, action_posters = get_action()
    romance_names, romance_posters = get_romance()
    crime_names, crime_posters = get_crime()

    return render_template('index2.html', top_names=top_names, top_posters=top_posters,
                           action_names = action_names, action_posters=action_posters,
                           romance_names = romance_names, romance_posters=romance_posters,
                           crime_names = crime_names, crime_posters=crime_posters)


@app.route('/info')
def movie_info():
    poster = fetch_poster(m_id)
    movie = movies_info[movies_info['id'] == m_id]
    title = movie['title'][ind]
    genre = movie['genres'][ind]
    overview = movie['overview'][ind]
    tagline = movie['tagline'][ind]
    cast1 = movie['cast'][ind][0]
    cast2 = movie['cast'][ind][1]
    cast3 = movie['cast'][ind][2]
    crew = movie['crew'][ind]
    runtime = movie['runtime'][ind]

    r_posters = recommend(title)
    for i in r_posters:
        print(i)

    return render_template('movie_info.html', title=title, poster=poster, genre=genre, tagline=tagline, crew=crew,
                           overview=overview, cast1=cast1, cast2=cast2, cast3=cast3, runtime=runtime,
                           r_posters=r_posters)


@app.route('/info', methods=['POST'])
def search():
    name = request.form['search']
    temp = movies[movies['title'] == name]
    print(name)
    ind = temp.index[0]
    m_id = movies.iloc[ind].id
    poster = fetch_poster(m_id)
    movie = movies_info[movies_info['id'] == m_id]
    title = movie['title'][ind]
    genre = movie['genres'][ind]
    overview = movie['overview'][ind]
    tagline = movie['tagline'][ind]
    cast1 = movie['cast'][ind][0]
    cast2 = movie['cast'][ind][1]
    cast3 = movie['cast'][ind][2]
    crew = movie['crew'][ind]
    runtime = movie['runtime'][ind]
    r_posters = recommend(title)
    return render_template('movie_info.html', title=title, poster=poster, genre=genre, tagline=tagline, crew=crew,
                           overview=overview, cast1=cast1, cast2=cast2, cast3=cast3, runtime=runtime,
                           r_posters=r_posters)


if __name__ == '__main__':
    # app = Flask(__name__, template_folder="template")
    app.run(debug=True)
