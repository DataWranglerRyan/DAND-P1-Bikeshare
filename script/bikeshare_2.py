from models.user_prompter import UserPrompter

prompt = UserPrompter()

city = prompt.get_city()
prompt.filter_month_and_day()
city.show_all_stats()

# print(city.filtered_df)
