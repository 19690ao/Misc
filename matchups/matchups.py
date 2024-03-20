import csv
import time
import os
import requests
from functools import reduce

class MatchupChart():
    def __init__(self, names, playrates, winrates) -> None:
        # print(names, playrates, winrates)
        self.names = names
        self.indices = {name: index for index, name in enumerate(self.names)}
        self.size = len(self.names)
        self.playrates = playrates
        self.matchup_data = {index: dict() for index in range(1, self.size)}
        for i in range(self.size):
            for j in range(i):
                # print(i,j)
                # print(winrates[i-1])                   
                self.matchup_data[i][j] = winrates[i-1][j]

    def get_winrate(self, a, b) -> float:
        i = self.indices[a]
        j = self.indices[b]
        # print(self.matchup_data)
        if i < j:
            return 1-self.matchup_data[j][i]
        if j < i:
            return self.matchup_data[i][j]
        else:
            return 0.5
        


    def load_matchup_data(file_path) -> "MatchupChart":
        with open(file_path, mode='r', newline='') as file:
            lines = list(csv.reader(file))
            names = lines[0]
            playrates = list(map(float, lines[1]))
            winrates = [list(map(float, line)) for line in lines[2:]]
        return MatchupChart(names, playrates, winrates)

def get_file_list(folder_path, file_name):
    # Join folder path and file name to create the full file path
    full_file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if os.path.exists(full_file_path):
        # Open the file and print each line
        with open(full_file_path, 'r') as file:
            file_content = file.read().strip()
            return [item for item in file_content.split('\n') if item]
    else:
        print(f"File '{file_name}' not found in the specified folder.")
        return None

def write_to_file(lst, folder, filename):
    # Create directory if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Full path to the file
    file_path = os.path.join(folder, filename)

    # Open the file in write mode ('w')
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write each item in the list to a new line in the file
        for item in lst:
            file.write(f"{item}\n")

def replace_https_with_http(url):
    if url.startswith('https://'):
        return url.replace('https://', 'http://')
    else:
        return url

def get_html_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises a HTTPError if the status is 4xx, 5xx
        time.sleep(1) # Wait for 1 second
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

def split_string(main_str, sub_str, bool_val):
    #if sub_str not in main_str: return None
    if bool_val:
        # Return everything before the substring
        return main_str.split(sub_str, 1)[0]
    else:
        # Return everything after the first occurrence of the substring
        idx = main_str.find(sub_str)
        if idx != -1:
            return main_str[idx + len(sub_str):]
        else:
            return main_str

def print_vert(lst):
    for item in lst:
        print(item)



def main():
    print("Starting...")

    # Example usage
    matchup_chart = MatchupChart.load_matchup_data('winrates.csv')
    print(matchup_chart.names)
    print(matchup_chart.playrates)
    print(matchup_chart.get_winrate("UCLA", "Richmond"))

    for start, i in enumerate(matchup_chart.names):
        for j in matchup_chart.names[start:]:
            # print(i, j)
            assert matchup_chart.get_winrate(i, j) == 1-matchup_chart.get_winrate(j, i)


if __name__ == "__main__":
    main()