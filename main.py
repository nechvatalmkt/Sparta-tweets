import tweepy
import datetime
import schedule
import time
import os

# Nastavení X API z proměnných prostředí
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)

# Datum a čas konce posledního zápasu
end_of_season = datetime.datetime(2025, 5, 24, 18, 0, 0)  # 24. 5. 2025, 18:00 CEST

# Funkce pro správné skloňování slova "den"
def sklonuj_dny(pocet_dnu):
    if pocet_dnu == 1:
        return "den"
    elif 2 <= pocet_dnu <= 4:
        return "dny"
    else:
        return "dní"

# Funkce pro odeslání tweetu
def send_tweet():
    now = datetime.datetime.now()
    time_diff = now - end_of_season
    days = time_diff.days
    dny_text = sklonuj_dny(days)  # Správné skloňování

    tweet = f"Už je to {days} {dny_text} od konce sezony @ACSparta_cz a stále nemáme trenéra."
    try:
        api.update_status(tweet)
        print(f"Tweet odeslán: {tweet}")
    except tweepy.TweepError as e:
        print(f"Chyba při odesílání tweetu: {e}")

# Plánování tweetu každý den v 18:00
schedule.every().day.at("18:00").do(send_tweet)

# Hlavní smyčka
while True:
    schedule.run_pending()
    time.sleep(60)  # Kontrola každou minutu
