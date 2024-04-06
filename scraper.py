from urllib.parse import urlencode
from requests import get as get_request
from bs4 import BeautifulSoup
from json import dumps as jsonify


# Header to prevent getting flagged as bot/spam/scraper instantly
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}


# get hotel info from booking.com as html
def get_hotel_info(
    query,
    checkin: str = "",
    checkout: str = "",
    number_of_rooms=1,
    number_of_adults: int = 2,
    offset: int = 0,
    result_count: int = 5,
):
    # split checkin and checkout dates
    checkin_year, checking_month, checking_day = checkin.split("-") if checkin else ("", "", "")
    checkout_year, checkout_month, checkout_day = checkout.split("-") if checkout else ("", "", "")

    # create url
    url = "https://www.booking.com/searchresults.html"
    url += "?" + urlencode(
        {
            "ss": "+".join(query.split()),
            "checkin_year": checkin_year,
            "checkin_month": checking_month,
            "checkin_monthday": checking_day,
            "checkout_year": checkout_year,
            "checkout_month": checkout_month,
            "checkout_monthday": checkout_day,
            "no_rooms": number_of_rooms,
            "group_adults": number_of_adults,
            "offset": offset,
        }
    )

    response = get_request(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")
    hotel_details_json = {}
    count = 0

    # get all hotel deatils
    hotels = soup.find_all("div", attrs={"data-testid": "property-card"})
    
    for hotel in hotels:
        try:
            name = hotel.find("div", attrs={"data-testid": "title"}).text
            price = int(hotel.find("span", attrs={"data-testid": "price-and-discounted-price"}).text[2:].replace(",", ""))
            review_score = hotel.find("div", attrs={"data-testid": "review-score"}).find_all("div")
            rating = float(review_score[0].find("div").text[7:])
            reviews = int(review_score[2].find_all("div")[1].text.replace(",", "")[:-8])
            room_details = hotel.find("div", attrs={"data-testid": "recommended-units"})
            room_type = room_details.find("h4").text
            bed_type = room_details.find("li").text
            img_src = hotel.find("img").get("src")
            
            hotel_details_json[count] = {
                "name": name,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "room_type": room_type,
                "bed_type": bed_type,
                "img_src": img_src
            }

            count += 1

            if count == result_count:
                break
        except AttributeError as e:
            continue
    
    # return hotel details
    return jsonify(hotel_details_json)

if __name__ == "__main__":
    print(get_hotel_info("Chandigarh", checkin="2024-11-08", checkout="2024-11-12", number_of_adults=15, number_of_rooms=6))