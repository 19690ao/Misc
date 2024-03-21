import csv
import time
import os
import requests

class MatchupChart():
    def __init__(self, names, playrates, winrates) -> None:
        # print(names, playrates, winrates)
        self.names = names
        self.indices = {name: index for index, name in enumerate(self.names)}
        self.size = len(self.names)
        assert self.size == len(playrates)
        self.playrates = playrates
        self.matchup_data = {i: {j: winrates[i-1][j] for j in range(i)} for i in range(1, self.size)}
        self.secondaries = [[[self.indices[name] for name in names] for names in self.get_secondaries(self.names[index])] for index in range(self.size)]
        self.tierlists = [[self.indices[name] for name in tierlist] for tierlist in self.get_tierlists()]

    def get_tierlists(self):
        data = {name: self.get_group_winrate([name]) for name in self.names}
        unweighted = sorted(self.names, key=lambda x: data[x][2], reverse=True)
        weighted = sorted(self.names, key=lambda x: data[x][3], reverse=True)
        return (unweighted, weighted)    

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

    def get_experience_coefficient(self, name, opponent):
        return self.get_playrate(name)/self.get_playrate(opponent)

    def load_matchup_data(file_path) -> "MatchupChart":
        with open(file_path, mode='r', newline='') as file:
            lines = list(csv.reader(file))
            names = lines[0]
            playrates = list(map(float, lines[1]))
            winrates = [list(map(float, line)) for line in lines[3:]]
        return MatchupChart(names, playrates, winrates)

    def get_playrate(self, name):
        assert name in self.names
        return self.playrates[self.indices[name]]

    def get_secondaries(self, name):
        assert name in self.names
        data = dict()
        other_names = []
        for secondary in self.names:
            if secondary == name: continue
            other_names.append(secondary)
            data[secondary] = self.get_group_winrate([name, secondary])
        unweighted_names = sorted(other_names, key=lambda x: data[x][0], reverse=True)
        weighted_names = sorted(other_names, key=lambda x: data[x][1], reverse=True)  
        exp_unweighted_names = sorted(other_names, key=lambda x: data[x][2], reverse=True)
        exp_weighted_names = sorted(other_names, key=lambda x: data[x][3], reverse=True)
        return (unweighted_names, weighted_names, exp_unweighted_names, exp_weighted_names)

    def get_group_winrate(self, names) -> tuple[float]:
        # print("RAW")
        # print([[self.get_winrate(name, opponent) for name in names] for opponent in self.names])
        maxed_winrates = [max(winrates) for winrates in [[self.get_winrate(name, opponent) for name in names] for opponent in self.names]]
        experienced_winrates = [max(winrates) for winrates in [[self.get_winrate(name, opponent)*self.get_experience_coefficient(name, opponent) for name in names] for opponent in self.names]]
        # print(maxed_winrates)
        unweighted = sum(maxed_winrates)/self.size
        weighted = sum([maxed_winrates[i]*self.playrates[i] for i in range(self.size)])
        experienced_unweighted = sum(experienced_winrates)/self.size
        experienced_weighted = sum([experienced_winrates[i]*self.playrates[i] for i in range(self.size)])
        return (unweighted, weighted, experienced_unweighted, experienced_weighted)
    
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

def write_and_print(text, file, end='\n'):
    # Write the text to the file
    file.write(text + end)
    # Print the text to the console
    print(text, end=end)


def main():
    print("Starting...")

    # Example usage
    matchup_chart = MatchupChart.load_matchup_data('winrates.csv')
    print(matchup_chart.names)
    print(matchup_chart.playrates)

    for start, i in enumerate(matchup_chart.names):
        for j in matchup_chart.names[start:]:
            assert matchup_chart.get_winrate(i, j) == 1-matchup_chart.get_winrate(j, i)

    with open("secondaries.txt", 'w') as file:
        c1_size = 20
        # c2_size = 12
        for name in matchup_chart.names:
            secondaries = matchup_chart.get_secondaries(name)
            write_and_print(f"{name}:", file)
            write_and_print("UNWEIGHTED:"+' '*(c1_size-11)+str(secondaries[0]), file)
            write_and_print("WEIGHTED:"+' '*(c1_size-9)+str(secondaries[1]), file)
            write_and_print("EXP UNWEIGHTED:"+' '*(c1_size-15)+str(secondaries[2]), file)
            write_and_print("EXP WEIGHTED:"+' '*(c1_size-13)+str(secondaries[2]), file)
            write_and_print('', file)
            

    with open("tierlists.txt", 'w') as file:
        c1_size = 6
        c2_size = 20
        tierlists = matchup_chart.get_tierlists()
        write_and_print("RANK"+' '*(c1_size-4)+"UNWEIGHTED"+' '*(c2_size-10)+"WEIGHTED", file)
        assert len(tierlists[0]) == len(tierlists[1])
        for i in range(len(tierlists[0])):
            write_and_print(str(i+1)+' '*(c1_size-len(str(i+1)))+tierlists[0][i]+' '*(c2_size-len(tierlists[0][i]))+tierlists[1][i], file)

    ans = matchup_chart.get_secondaries(input("What Character?\n>> ").upper())
    print(*ans, sep='\n')
    

if __name__ == "__main__":
    main()