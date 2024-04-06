from openai import OpenAI



ITINERARY_GENERATION_PROMPT_SAMPLE_INPUT = {
    "start_location": "New York",
    "end_location": "Los Angeles",
    "budget": 30000,
    "start_date": "2024-04-14",
    "end_date": "2024-04-16",
    "group_size": 4,
    "mode_of_arrival": "Flight",
    "mode_of_transport": "Rental Car",
    "accommodation": "Hotel",
    "activities": ["Sightseeing", "Hiking", "Shopping", "Clubbing"],
    "food_preference": ["Vegan", "Vegetarian", "Chinese", "Italian"],
    "day_wise_plan": {
        1: {
            (None, 17): "Reach New York Airport",
            (18, 20): "Flight to Los Angeles",
            (20, 21): "Get to Hotel Nova and check-in",
            (21, 22): "Dinner",
        },
        2: {
            (9, 10): "Breakfast",
            (10, 12): "Sightseeing",
            (12, 13): "Lunch",
            (13, 15): "Hiking",
            (15, 16): "Snacks",
            (18, 19): "Dinner",
            (22, None): "Clubbing",
        },
        3: {
            (9, 10): "Breakfast",
            (10, 12): "Shopping",
            (12, 13): "Lunch",
            (15, 16): "Snacks",
            (None, 17): "Reach Los Angeles Airport",
            (18, 20): "Flight to New York",
        },
    },
    "extra_information": "The group is traveling for a vacation and wants to explore the city."
}


def format_time(time):
    if time == 12:
        return f"{time} PM"
    elif time == 0:
        return "12 AM"
    elif time > 12:
        return f"{time - 12} PM"
    else:
        return f"{time} AM"
    

def parse_day_wise_plan(day_wise_plan: dict) -> str:
    DAY_WISE_PLAN_TEMPLATE = ""
    if day_wise_plan:
        DAY_WISE_PLAN_TEMPLATE = "Day Wise Plan:"
        for day, activities in day_wise_plan.items():
            DAY_WISE_PLAN_TEMPLATE += f"\nDay {day}:"
            for timestamp, activity in activities.items():
                if timestamp[0] is None:
                    DAY_WISE_PLAN_TEMPLATE += f"\nBy {format_time(timestamp[1])}: {activity}"
                elif timestamp[1] is None:
                    DAY_WISE_PLAN_TEMPLATE += f"\nFrom {format_time(timestamp[0])}: {activity}"
                else:
                    DAY_WISE_PLAN_TEMPLATE += f"\nFrom {format_time(timestamp[0])} to {format_time(timestamp[1])}: {activity}"
            DAY_WISE_PLAN_TEMPLATE += "\n"
    return DAY_WISE_PLAN_TEMPLATE


def generate_itinerary_prompt(itinerary_generation_input):
    # define docstring user inputs
    start_location = itinerary_generation_input['start_location']
    end_location = itinerary_generation_input['end_location']
    budget = itinerary_generation_input['budget']
    start_date = itinerary_generation_input['start_date']
    end_date = itinerary_generation_input['end_date']
    group_size = itinerary_generation_input['group_size']
    mode_of_arrival = itinerary_generation_input['mode_of_arrival']
    mode_of_transport = itinerary_generation_input['mode_of_transport']
    accommodation = itinerary_generation_input['accommodation']
    activities = ", ".join(itinerary_generation_input['activities'])
    food_preference = ", ".join(itinerary_generation_input['food_preference'])
    try:
        day_wise_plan = parse_day_wise_plan(itinerary_generation_input['day_wise_plan'])
    except KeyError:
        day_wise_plan = ""
    try:
        extra_information = itinerary_generation_input['extra_information']
    except KeyError:
        extra_information = ""

    # define prompt
    ITINERARY_GENERATION_PROMPT = f"""
Start Location: {start_location}
End Location: {end_location}
Budget: {budget}
Start Date: {start_date}
End Date: {end_date}
Group Size: {group_size}
Mode of Arrival: {mode_of_arrival}
Mode of Transport: {mode_of_transport}
Accommodation: {accommodation}
Activities: {activities}
Food Preferences: {food_preference}
{day_wise_plan}
{extra_information}

Start location is where the group will start the trip from.
End location is where the group is going for the trip.
Budget is the total amount of money the group has for the trip.
Start date is the date when the group will start the trip. It is in the format YYYY-MM-DD.
End date is the date when the group will end the trip. It is in the format YYYY-MM-DD.
Group size is the number of people in the traveling group.
Mode of arrival is how the group will reach the destination to start the trip.
Mode of transport is how the group plans on traveling around the destination during the trip.
Accommodation is where the group will stay during the trip.
Activities are the things the group will do at the destination during the trip.
Food preference is what kind of food the members of the group want to eat during the trip.
The day wise plan is optional, it will be the day-wise breakdown of the trip. It will include the activities planned for each day along with the timings. If the day-wise plan is not provided, you can skip that part.
Extra information is any additional optional information that should be considered as it adds more context to the trip.
The format of the itinerary is as follows:

1. Basic Information: Start Location, destination, budget, start date, end date, group size
2. Travel Information: Mode of arrival and mode of transport with potential cost
3. Accommodation Information: Accommodation plans and potential cost
4. Activity Information: Activities planned and potential cost
5. Food Preferences: All available food cuisines near the accommodation/stay along with their average cost of the meal
7. Important Documents: What documents the group needs to carry and where they can be required.
8. Timeline: Generate a rough timeline of the entire trip. Include the activities planned on each day and the where the group will stay for the night.
9. Suggestions: Give brief information of the following:
    a. Medical facilities available near the accommodation
    b. Local language of the destination 
    c. Frequent crimes that happen in that area along with crime rate
"""

    return ITINERARY_GENERATION_PROMPT


def create_itinerary(itinerary_generation_input):
    prompt = generate_itinerary_prompt(itinerary_generation_input)
    role_content = """You are a professional travel guide. You have been tasked to create an itinerary for a trip that has already been planned.
You are not supposed to suggest any changes to the trip plan. You are only supposed to create an itinerary for the given trip details.
When the information about the trip is shared, make an itinerary based on the format given."""
    client = OpenAI(api_key="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")

    try:
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_content},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message['content']
    except Exception as e:
        with open("create_itinerary_prompt.txt", "w") as f:
            f.write(role_content + "\n" + prompt)
    

if __name__ == "__main__":
    print(create_itinerary(ITINERARY_GENERATION_PROMPT_SAMPLE_INPUT))