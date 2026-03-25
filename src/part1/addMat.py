def longJourney(AList):
    # memo stores the longest path starting from a specific city
    memo = {}

    def find_path_from(city):
        # If we already calculated the longest path from this city, return it
        if city in memo:
            return memo[city]

        best_sub_path = []

        # Look at all cities reachable from here (to the south)
        # AList.get(city, []) handles cities with no outgoing routes
        for neighbor in AList.get(city, []):
            current_sub_path = find_path_from(neighbor)

            # We want the sub-path with the most cities
            if len(current_sub_path) > len(best_sub_path):
                best_sub_path = current_sub_path

        # The longest path from THIS city is the city itself + the best sub-path
        memo[city] = [city] + best_sub_path
        return memo[city]

    overall_longest_path = []

    # The longest journey could start at any city in the graph
    for start_city in AList:
        path = find_path_from(start_city)
        if len(path) > len(overall_longest_path):
            overall_longest_path = path

    return overall_longest_path


# --- Example Usage ---
# Adjacency List: Delhi -> Agra, Delhi -> Jaipur, Agra -> Gwalior, etc.
routes = {
    "Delhi": ["Agra", "Jaipur"],
    "Jaipur": ["Bhopal"],
    "Agra": ["Gwalior"],
    "Gwalior": ["Bhopal"],
    "Bhopal": ["Mumbai", "Hyderabad"],
    "Mumbai": ["Bengaluru"],
    "Hyderabad": ["Bengaluru"],
    "Bengaluru": ["Kanyakumari"],
    "Kanyakumari": []
}

print(longJourney(routes))
