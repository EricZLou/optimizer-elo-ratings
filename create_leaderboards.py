import json
import os
from pprint import pprint


THIS_PATH = os.path.dirname(os.path.realpath(__file__))
OPTIMIZER_ELO_PATH = THIS_PATH + os.path.sep + 'results'

def load_all_games():
    def load_json(file):
        with open(os.path.join(OPTIMIZER_ELO_PATH, file), "r") as f:
            ret = json.load(f)
        return ret

    games = list()
    i = 0
    leaderboard_jsons = dict(
        (file, load_json(file)) for file in os.listdir(OPTIMIZER_ELO_PATH) if os.path.isfile(
            os.path.join(OPTIMIZER_ELO_PATH, file)
        ) and os.path.join(OPTIMIZER_ELO_PATH, file).endswith(".json")
    )
    return leaderboard_jsons               # "name" and "rating" keys are important

def get_html_table_rows(data):
    data_dict = {}
    for name, rating in zip(data["name"], data["rating"]):
        data_dict[name] = rating

    data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

    html = "<tr><th>Name</th><th>Rating</th></tr>"
    for name, rating in data_dict.items():
        html += f"<tr><td>{name}</td><td>{round(rating, 3)}</td></tr>"
    return html

# For overall.json
def get_overall_html_str(file, data, navbar):
    return f"""<html>
<head><link rel="stylesheet" href="../style.css" type="text/css"></head>
<body>
    <div class="left">{navbar}</div>
    <div class="right">
        <h1>Overall Optimizer Elo Leaderboard for {file}</h1>
        <table class="default-table">
            {get_html_table_rows(data)}
        </table>
    </div>
</body>
</html>"""

# For all the other jsons
def get_html_str(file, data, navbar):
    parse_file = file.replace(".json", "")
    args = parse_file.split("_")

    return f"""<html>
<head><link rel="stylesheet" href="../style.css" type="text/css"></head>
<body>
    <div class="left">{navbar}</div>
    <div class="right">
        <h1>Optimizer Elo Leaderboard for {file}</h1>
        <h3>Set of optimizers: {args[0]}</h3>
        <h3>Number of dimensions: {args[1][1:]}</h3>
        <h3>Max number of evaluations: {args[2][1:]}</h3>
        <table class="default-table">
            {get_html_table_rows(data)}
        </table>
    </div>
</body>
</html>"""

def get_html_navbar(json_names):
    div = "<h3>Leaderboards</h3>"
    for name in json_names:
        name_html = name.replace(".json", ".html")
        div += f"<a href='{name_html}'>{name}</a>"
    return div

# For index.html
def get_index_html_str(json_names):
    navbar = "<h3>Leaderboards</h3>"
    for name in json_names:
        name_html = name.replace(".json", ".html")
        navbar += f"<a href='html_leaderboards/{name_html}'>{name}</a>"
    return f"""<html>
<head><link rel="stylesheet" href="style.css" type="text/css"></head>
<body>
    <div class="left">
        {navbar}
    </div>
</body>
</html>"""

if __name__ == '__main__':
    jsons = load_all_games()

    HTML_DIR = os.path.join(THIS_PATH, "docs", "html_leaderboards")
    if not os.path.exists(HTML_DIR):
        os.mkdir(HTML_DIR)

    with open(os.path.join(THIS_PATH, "docs", "index.html"), "w") as f:
        f.write(get_index_html_str(jsons.keys()))

    navbar = get_html_navbar(jsons.keys())
    for file, data in jsons.items():
        file_html = file.replace(".json", ".html")
        with open(os.path.join(HTML_DIR, file_html), "w") as f:
            if file == "overall.json":
                f.write(get_overall_html_str(file, data, navbar))
            else:
                f.write(get_html_str(file, data, navbar))
