FEATURE_COLUMNS = [
    "sleep_hours",
    "exercise_minutes",
    "water_intake_liters",
    "stress_level",
    "screen_time_hours",
    "smoker",
    "alcohol_use",
    "diet_quality",
    "fruits_per_day",
    "vegetables_per_day"
]


def build_feature_vector(data):
    return [[
        data.sleep_hours,
        data.exercise_minutes,
        data.water_intake_liters,
        data.stress_level,
        int(data.screen_time_hours),
        int(data.smoker),
        int(data.alcohol_use),
        data.diet_quality,
        data.fruits_per_day,
        data.vegetables_per_day
    ]]