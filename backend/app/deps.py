"""
Temporary auth stand-in until a real login/JWT flow exists.

get_current_user() returns a fixed mock student profile shaped like the
eventual student profile fields from the design doc (year, branch,
interests, hobbies, reason - see the plan's "Required schema additions"
section). year/branch already exist on the Student model; interests/hobbies/
reason do not yet, so this fills them in until that migration lands.

interests/hobbies/reason are left empty on purpose: this stub has no real
student behind it, so any placeholder values here would silently bias every
club-finder request toward the same clubs regardless of what a caller types.
The one live signal (branch) stays, since it is a real Student column.

Replace this with a real dependency that decodes a session/JWT and loads the
Student row (plus the new profile columns) once auth and the schema
migration exist. Every caller only depends on the dict shape below.
"""
from __future__ import annotations


def get_current_user() -> dict:
    return {
        "id": 1,
        "college_id": 1,
        "full_name": "Test Student",
        "branch": "cse",
        "year": 2,
        "interests": [],
        "hobbies": [],
        "reason": "",
    }
