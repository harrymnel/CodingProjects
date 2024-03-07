import requests
import webbrowser

def get_random_meal():
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    data = response.json()
    return data['meals'][0] if data['meals'] else None

def display_meal_details(meal):
    print("Recipe Name:", meal['strMeal'])
    print("Ingredients:")
    for i in range(1, 21):
        ingredient = meal[f'strIngredient{i}']
        measure = meal[f'strMeasure{i}']
        if ingredient and measure:
            print(f"- {ingredient}: {measure}")
    print("\nInstructions:", meal['strInstructions'])
    print("Meal Picture URL:", meal['strMealThumb'])
    video_url = meal['strYoutube']
    if video_url:
        print("YouTube Video URL:", video_url)
        webbrowser.open(video_url)

def main():
    input("Press Enter to generate a random meal...")
    meal = get_random_meal()
    if meal:
        print("\nRandom Meal Details:")
        display_meal_details(meal)
    else:
        print("Failed to retrieve a random meal.")

if __name__ == "__main__":
    main()

