import requests
from bs4 import BeautifulSoup
from datetime import datetime

URLS = {
    "Büyükada to Bostancı": "https://mavimarmara.net/tarifeler/buyukada-bostanci/",
    "Bostancı to Büyükada": "https://mavimarmara.net/tarifeler/bostanci-buyukada/"
}
OUTPUT_FILE = "schedule.txt"

def is_sunday():
    """Bugünün Pazar olup olmadığını kontrol eder."""
    return datetime.today().weekday() == 6  # 6 = Pazar

def scrape_schedule():
    schedule = []
    today_is_sunday = is_sunday()

    for route, url in URLS.items():
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Sayfa yüklenemedi: {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")

        schedule.append(route)  # Başlık ekle

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                time_text = cells[0].get_text(strip=True)  # Saat
                route_text = cells[1].get_text(strip=True)  # Varış noktası

                # Saat formatı kontrolü (hh:mm gibi olmalı)
                if ":" not in time_text:
                    continue  # Saat formatında değilse atla

                # Eğer saatin yanında `*` varsa ve bugün Pazar ise, atla
                if "*" in time_text:
                    if today_is_sunday:
                        continue
                    time_text = time_text.replace("*", "").strip()  # `*` işaretini temizleyip boşlukları da kaldır

                schedule.append(f"{time_text} - {route_text}")

        schedule.append("")  # Boş satır ekle (daha okunaklı olsun)

    if schedule:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(schedule))
        print("Saatler ve güzergahlar kaydedildi.")
    else:
        print("Saat ve güzergah bilgisi bulunamadı.")

if __name__ == "__main__":
    scrape_schedule()
