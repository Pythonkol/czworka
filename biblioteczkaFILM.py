
import random
from datetime import date

class Movie:
    def __init__(self, title, year, film_genre, play=0):
        self.title = title
        self.year = year
        self.genre = film_genre
        self.plays = play

    def __str__(self):
        return f"{self.title} ({self.year})"

    def play(self, step=1):
        self.plays += step

class Series(Movie):
    def __init__(self, title, year, film_genre, season, episode, play=0):
        super().__init__(title, year, film_genre, play)
        self.season = season
        self.episode = episode

    def __str__(self):
        return f"{self.title} S{self.season:02}E{self.episode:02}"

biblio = []

def get_movies():
    return sorted([item for item in biblio if isinstance(item, Movie) and not isinstance(item, Series)],
         key=lambda x: x.title)

def get_series():
    return sorted([item for item in biblio if isinstance(item, Series)],
         key=lambda x: x.title)

def search(title):
    return [item for item in biblio if title.lower() in item.title.lower()]

def generate_views():
    item = random.choice(biblio)
    views = random.randint(1, 100)
    item.play(views)

def run_generate_views(times=10):
    for _ in range(times):
        generate_views()

def top_titles(number=3, content_type=None):
    if content_type == "movie":
        items = get_movies()
    elif content_type == "series":
        items = get_series()
    else:
        items = biblio
    return sorted(items, key=lambda x: x.plays, reverse=True)[:number]

if __name__ == "__main__":
    print("Biblioteka filmów\n")

    biblio.append(Movie("Pulp Fiction", 1994, "Crime"))
    biblio.append(Movie("Skazani na Shawshank", 1994, "Drama"))
    biblio.append(Movie("Gladiator", 2000, "History"))
    biblio.append(Movie("Shrek", 2001, "Family"))
    biblio.append(Series("Friends", 1994, "Comedy", 1, 1))
    biblio.append(Series("Friends", 1996, "Comedy", 1, 2))
    biblio.append(Series("Friends", 1998, "Comedy", 1, 5))

    run_generate_views(10)

    today = date.today().strftime("%d.%m.%Y")
    print(f"TOP filmy i seriale z dnia {today}:\n")
    for item in top_titles(3):
        print(f"{item} — {item.plays} wyświeleń")



