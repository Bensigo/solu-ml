
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from app.utils.supabase import article_table

class Recommender:
    def __init__(self, data):
        self.data = data
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self._compute_tfidf_matrix()

    def _compute_tfidf_matrix(self):
        if len(self.data) == 0:
            return None
        # Join the lists of tags into a single string for each article
        self.data['tags'] = self.data['tags'].apply(lambda x: ' '.join(x))
        return self.tfidf_vectorizer.fit_transform(self.data['tags'])

    def get_recommendations(self, input_tags, num_recommendations=10):
        if len(self.data) == 0:
            return None
        input_tags_str = ' '.join(input_tags)
        print(input_tags_str)
        input_vec = self.tfidf_vectorizer.transform([input_tags_str])
        sim_scores = list(enumerate(cosine_similarity(input_vec, self.tfidf_matrix)[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1]
        items_indices = [i[0] for i in sim_scores]
        return self.data.iloc[items_indices]




def get_article_df():
    # todo: find better way of getting data or doing the query 
    articles = article_table.select('*').execute()
    df = pd.DataFrame(articles.data)
    return df


