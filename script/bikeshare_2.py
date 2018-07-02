from models.user_prompter import UserPrompter

prompt = UserPrompter()

city = prompt.get_city()
prompt.filter_month_and_day()
city.show_popular_travel_times()
city.show_popular_stations()
city.show_trip_duration_stats()

# print(city.filtered_df)
