"""
Temporary auth stand-in until a real login/JWT flow exists.

get_current_user() returns a fixed mock student shaped to the REAL schema
(campus_connect_schema.md): users has college_id + full_name; students has
bio, branch, year. There are deliberately NO interests / hobbies / reason
columns - the earlier plan proposed them but the final schema does not have
them, so the recommender's interest signal comes from:
  - what the student types into the finder (interest_text, added per request
    in routers/ai.py), and
  - the student's free-text bio (mapped onto the profile's "reason" slot,
    which profile_tokens() already tokenises).
branch and year are real student columns and are passed through as-is.

Replace this with a real dependency that decodes a session/JWT and loads the
User + Student rows once auth exists. Every caller depends only on the dict
shape below.
"""
from __future__ import annotations


def get_current_user() -> dict:
    return {
        "id": 1,
        "college_id": 1,
        "full_name": "Test Student",
        "bio": "",
        "branch": "cse",
        "year": 2,
    }
