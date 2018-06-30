from models.user_prompter import UserPrompter
print("hello world")
prompt = UserPrompter()

city = prompt.get_city()
prompt.filter_month_and_day()
city.show_popular_travel_times()

# print(city.filtered_df)
