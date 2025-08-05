# utils.py

def format_user_profile(profile: dict) -> str:
    """
    Convert user profile dictionary into a readable string format.
    Useful for prompt generation and UI display.
    """
    if not profile:
        return "No profile data available."
    
    return "\n".join([f"{key.capitalize()}: {value}" for key, value in profile.items()])


def validate_input(data: dict, required_fields: list) -> bool:
    """
    Check if all required fields are present and non-empty.
    Returns True if valid, False otherwise.
    """
    return all(data.get(field) for field in required_fields)


def calculate_match_score(profile1: dict, profile2: dict) -> int:
    """
    Dummy matching algorithm to calculate compatibility score.
    You can replace this with advanced AI/LLM logic.
    """
    score = 0
    total = len(profile1)

    for key in profile1:
        if profile1[key].lower().strip() == profile2.get(key, "").lower().strip():
            score += 1

    return int((score / total) * 100) if total > 0 else 0


def highlight_match(score: int) -> str:
    """
    Return a feedback message based on match score.
    """
    if score >= 80:
        return "💖 Perfect Match!"
    elif score >= 60:
        return "😊 Good Match"
    elif score >= 40:
        return "🤔 Possible Match"
    else:
        return "❌ Not Compatible"
