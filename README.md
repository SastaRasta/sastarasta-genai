### Module-wise documentation for use
- import module using import module_name
- for example: import scraper

## How to use scraper.py
### get_hotel_details()
* Function to return a JSON file with details of hotels from booking.com
* Input
    - city: name of city ("Ghaziabad")
    - checkin: date of checking in ("2024-04-05")
    - checkout: date of checking out ("2024-04-07")
    - number_of_rooms: integer count of number of rooms (6)
    - number_of_adults: integer count of number of adults/members in group (15)
    - result_count: integer count of max number of json records to return (7)
* Output
    - name: name of hotel,
    - price: total price of stay from checkin to checkout,
    - rating: rating of hotel,
    - reviews: number of reviews for the hotel,
    - room_type: type of hotel room,
    - bed_type: type and count of beds in room,
    - img_src: hotel image source location