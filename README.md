# Module-wise documentation for use
- import module using import module_name
- for example: import scraper

## How to use scraper.py
### get_hotel_details()
* Function to return a JSON file with details of hotels from booking.com
* Input
    - city: name of city (String)
    - checkin: date of checking in (String, "YYYY-MM-DD")
    - checkout: date of checking out (String, "YYYY-MM-DD")
    - number_of_rooms: integer count of number of rooms (Integer)
    - number_of_adults: integer count of number of adults/members in group (Integer)
    - result_count: integer count of max number of json records to return (Integer)
* Output
    - name: name of hotel (String)
    - price: total price of stay from checkin to checkout (Integer)
    - rating: rating of hotel (Float)
    - reviews: number of reviews for the hotel (Integer)
    - room_type: type of hotel room (String)
    - bed_type: type and count of beds in room (String)
    - img_src: hotel image source location (String)

## How to use prompt.py
### create_itinerary()
* Function returns JSON file containing the response of the language model which is the content of an itinerary
* Input (a JSON file)
    - start_location: The string location where journey begins (String)
    - end_location: The location where the trip is (String)
    - budget: The total budget of all members combined (Integer)
    - start_date: The date the trip begins (String, "YYYY-MM-DD")
    - end_date: The date the trip ends (String, "YYYY-MM-DD")
    - group_size: The number of people going on the trip (Integer)
    - mode_of_arrival: The transport used to reach the end location (String)
    - mode_of_transport: The transport used to travel around the destination location (String)
    - accomodation: The type of lodging where the travel group is staying (String)
    - activities: List of activities planned for the trip (List of Strings)
    - day_wise_plan: A JSON where key is the day number and value is another JSON in which key is a tuple of 2 integers that represent time and the value is the name of the activity. The first value in tuple is activity start time and second value is end time (JSON of Integer key and JSON value of Integer tuple of size 2 for ke and String as value)
    - extra_information: Extra information for adding context to trip planning for nuanced details (String)
