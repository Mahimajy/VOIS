#importing required library

import streamlit as st

import pandas as pd

import difflib

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity



# loading the data from the csv file to apandas dataframe

movies_data = pd.read_csv(r"C:\Users\hp\Downloads\movies.csv")



# selecting the relevant features for recommendation

selected_features = ['genres','keywords','tagline','cast','director']



# replacing the null valuess with null string

for feature in selected_features:

    movies_data[feature] = movies_data[feature].fillna('')



# combining all the 5 selected features

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']



#vectorizing all 5 combined features

vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vectors)





def main_page(): #first page of the streamlit

    #introducing and page title

    st.sidebar.markdown("Introduction")

    st.sidebar.markdown("This is a movie recommender system introduction page")

    st.title('Movie Recommender System')

    st.write("This movie recommendation system contains 2 sections, section 1 contains single input and section 2 contains multiple input")

    st.write("the method we used in this is TF-IDF vectorizer and content based filtering")



def page2():

    st.sidebar.markdown("Movie recommendation system by taking 1 input movie name")

    st.sidebar.markdown("This will take a movie name as a input")

    st.sidebar.markdown("This is a movie recommender system using TF-IDF. This will take a movie name from the user and will find the index of that movie from dataset and the recommender system will give the output of nearest movie indexes and from that nearest indexes the system will find the movie name from dataset and arrange it in descending order")

    

    st.title('Movie Recommender System using TF-IDF')

    movies_data = pd.read_csv(r"C:\Users\hp\Downloads\movies.csv")

    c=st.selectbox("Enter a movie name",movies_data['title'].values)

        

    if st.button('Recommend'):        

        movie_name = c

        list_of_all_titles = movies_data['title'].tolist()

        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

        close_match = find_close_match[0]

        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

        similarity_score = list(enumerate(similarity[index_of_the_movie]))

        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

        st.write('Movies suggested for you : \n')

        i = 0

        for movie in sorted_similar_movies:

            index = movie[0]

            title_from_index = movies_data[movies_data.index==index]['title'].values[0]

            i+=1

            if i>= 2:

                st.write(title_from_index)

            if i==6:

                break        



def page3():

    st.sidebar.markdown("Movie recommendation system by taking multiple input movie name")

    st.sidebar.markdown("This will take multiple movie names as a input")

    st.sidebar.markdown("This is a movie recommender system using TF-IDF. This will take a list of movie names from the user and will find the index of that movie from dataset and the recommender system will give the output of nearest movie indexes and from that nearest indexes the system will find the movie name from dataset and arrange it in descending order")

    ist=[]

    st.title('Movie Recommender System using TF-IDF (enhanced)')

    movies_data = pd.read_csv(r"C:\Users\hp\Downloads\movies.csv")

    c=st.multiselect("Enter more than one movie names",movies_data['title'].values)

    if st.button('Recommend'): 

        c=list(c)

        for ele in c:

            movie_name = ele

            list_of_all_titles = movies_data['title'].tolist()

            find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

            close_match = find_close_match[0]

            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

            similarity_score = list(enumerate(similarity[index_of_the_movie]))

            sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

            i = 0

            for movie in sorted_similar_movies:

                index = movie[0]

                title_from_index = movies_data[movies_data.index==index]['title'].values[0]

                i+=1

                if i>= 2:

                    ist.append(title_from_index)

                if i==6:

                    break

        result = sorted(ist, key = ist.count, reverse = True)

        res = [i for n, i in enumerate(result) if i not in result[:n]]

        for i in res[:]:

                if i in c:

                    res.remove(i)

        for i in res:

            st.write(i)



page_names_to_funcs = {

    "main page": main_page,

    "Single input TF-IDF": page2,

    "Multiple input TF-IDF": page3,

}



selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())

page_names_to_funcs[selected_page](
