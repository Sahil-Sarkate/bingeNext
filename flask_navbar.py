# from flask import Flask, render_template, request
# from flask_navigation import Navigation
#
# import requests
# import pickle
# import pandas as pd
#
# app = Flask(__name__)
# nav = Navigation(app)
#
#
# # @app.route('/')
# # def index():
# #     return render_template('index.html')
#
#
# @app.route('/navpage')
# def navpage():
#     return render_template('navpage.html')
#
#
# def fetch_poster(movie_id):
#     response = requests.get(
#         'https://api.themoviedb.org/3/movie/{}?api_key=93a8bfabeddaf037b287771c8ae3e4fe&language=en-US'.format(
#             movie_id))
#     data = response.json()
#     url = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
#     return url
#
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movie_list:
#         movie_id = movies.iloc[i[0]].id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies_posters
#
#
# def get_action():
#     action_posters = [None]*20
#     action_list = movies[movies['genres'] == 'Action']
#     action_list = action_list.head(20)
#     for i in action_list:
#         movie_id = action_list.iloc[i].id
#         action_posters.append(fetch_poster(movie_id))
#
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# movies_dict = pickle.load(open('movies.pkl', 'rb'))
# movies_info = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
#
# @app.route('/')
# def index():
#     posters = recommend('Avatar')
#     action_posters = get_action()
#     return render_template('index.html', action_posters=action_posters)
#
#
# # @app.route('/')
# # def search():
# #     name = request.form.get("searchbar")
# #     temp = movies[movies['title'] == name].index[0]
# #     id = movies.iloc[temp[0]]
# #     url = fetch_poster(id)
#
# # if st.button('Recommend'):
# #     names, posters = recommend(selected_movie)
# #     col1, col2, col3, col4, col5 = st.columns(5)
# #     with col1:
# #         st.text(names[0])
# #         st.image(posters[0])
# #     with col2:
# #         st.text(names[1])
# #         st.image(posters[1])
# #
# #     with col3:
# #         st.text(names[2])
# #         st.image(posters[2])
# #     with col4:
# #         st.text(names[3])
# #         st.image(posters[3])
# #     with col5:
# #         st.text(names[4])
# #         st.image(posters[4])
#
#
# if __name__ == '__main__':
#     # app = Flask(__name__, template_folder="template")
#     app.run(debug=True)
