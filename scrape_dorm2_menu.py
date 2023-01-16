import requests
import json
import calendar


def main():
    weekly_menu = fetch_weekly_menu()
    for i, menu in enumerate(weekly_menu):
        day_name = calendar.day_name[i]
        date = menu["date"]
        breakfast = menu["breakfast"]
        lunch_cheap = menu["lunch"]["cheap"]
        lunch_expensive = menu["lunch"]["expensive"]
        dinner = menu["dinner"]

        print(
            f"{day_name} {date}\n"
            f"Breakfast: {breakfast}\n"
            f"Lunch:\n"
            f"    Cheap: {lunch_cheap}\n"
            f"    Expensive: {lunch_expensive}\n"
            f"Dinner: {dinner}\n"
            f""
        )


def fetch_weekly_menu() -> list[dict]:
    weekly_menu_data = fetch_raw_weekly_menu_data()
    weekly_menu = [
        {
            "date": None,
            "breakfast": None,
            "lunch": {"cheap": None, "expensive": None},
            "dinner": None,
        }
        for _ in range(7)
    ]

    for k, v in weekly_menu_data.items():
        if k.startswith("fo_date"):
            day = int(k[-1]) - 1
            weekly_menu[day]["date"] = v
        elif k.startswith("fo_menu_mor"):
            day = int(k[-1]) - 1
            weekly_menu[day]["breakfast"] = v
        elif k.startswith("fo_menu_lun"):
            day = int(k[-1]) - 1
            weekly_menu[day]["lunch"]["cheap"] = v
        elif k.startswith("fo_sub_lun"):
            day = int(k[-1]) - 1
            weekly_menu[day]["lunch"]["expensive"] = v
        elif k.startswith("fo_menu_eve"):
            day = int(k[-1]) - 1
            weekly_menu[day]["dinner"] = v

    return weekly_menu


def fetch_raw_weekly_menu_data() -> dict[str, str]:
    URL = "https://dorm2.khu.ac.kr/food/getWeeklyMenu.kmc"
    POST_DATA = {
        "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "locgbn": "K1",
        "sch_date": "",
        "fo_gbn": "stu",
    }
    response = requests.post(URL, data=POST_DATA)

    weekly_menu_data = json.loads(response.text)
    weekly_menu_data = weekly_menu_data["root"][0]["WEEKLYMENU"][0]
    return weekly_menu_data


if __name__ == "__main__":
    main()
