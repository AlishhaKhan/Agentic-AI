import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def load_profiles(json_path="data/profiles.json"):
    """
    Load existing profiles from a JSON file.
    
    Args:
        json_path (str): Path to the profiles.json file.
    
    Returns:
        list: A list of user profiles (dicts).
    """
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Could not find file at: {json_path}")
    except json.JSONDecodeError:
        raise ValueError("❌ Failed to decode JSON. Check your file formatting.")


def compute_similarity(user_bio, profiles):
    """
    Compute cosine similarity between the user's bio and each profile's bio.

    Args:
        user_bio (str): The user's bio text.
        profiles (list): List of profiles with 'bio' field.

    Returns:
        list: Similarity scores between user bio and profile bios.
    """
    bios = [profile['bio'] for profile in profiles]
    all_bios = [user_bio] + bios  # Combine for joint vectorization

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_bios)

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarities


def find_matches(user_input, profiles, top_n=3):
    """
    Find top N most similar matches for the user.

    Args:
        user_input (dict): Dictionary containing user's 'bio' key.
        profiles (list): List of profile dictionaries with 'bio' key.
        top_n (int): Number of top matches to return.

    Returns:
        list: List of matched profiles sorted by similarity score.
    """
    similarities = compute_similarity(user_input['bio'], profiles)

    # Add similarity score to each profile
    for i, score in enumerate(similarities):
        profiles[i]['score'] = round(score * 100, 2)  # Percent format

    # Sort by score descending and return top N matches
    matches = sorted(profiles, key=lambda x: x['score'], reverse=True)[:top_n]
    return matches
