from flask import Flask, render_template, request  # Import request from flask, not requests
import pickle
import numpy as np

# Load the pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    # fetching user input from form
    user_input = request.form.get('user_input')

    # Check if the user input exists in the pivot table (pt)
    if user_input not in pt.index:
        return f"Book '{user_input}' not found in the database."

    # fetching the index of the book
    index = np.where(pt.index == user_input)[0][0]

    # Get the similarity scores and sort them
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        # Fetch book details for the similar items
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        
        # Collect book title, author, and image URL
        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]
        
        data.append(item)
    
    # Render the recommendations in the same UI
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
