import re

# sitemap.xml faylını oxu
with open("sitemap.xml", "r", encoding="utf-8") as f:
    content = f.read()

# URL dəyişmə mapping (köhnə -> yeni)
replacements = {
    "https://viktoria-az.store/bloq10.html": "https://viktoria-az.store/paltarlarin-evde-renglenmesi",
    "https://viktoria-az.store/bloq9.html": "https://viktoria-az.store/qara-sinka-paltar-uchun",
    "https://viktoria-az.store/bloq8.html": "https://viktoria-az.store/geyim-ve-tekstil-boyasi",
    "https://viktoria-az.store/bloq7.html": "https://viktoria-az.store/paltar-boyasi-hardan-almaq-olar",
    "https://viktoria-az.store/bloq6.html": "https://viktoria-az.store/paltar-boyasi-online-sifaris",
    "https://viktoria-az.store/bloq5.html": "https://viktoria-az.store/boyanin-istifade-qaydalari",
    "https://viktoria-az.store/bloq4.html": "https://viktoria-az.store/qaliciliga-tesir-eden-amiller",
    "https://viktoria-az.store/bloq3.html": "https://viktoria-az.store/sabitlesdirici-nece-istifade-olunur",
    "https://viktoria-az.store/bloq2.html": "https://viktoria-az.store/paltaryuyan-masinda-istifade-qaydalari",
    "https://viktoria-az.store/bloq1.html": "https://viktoria-az.store/qabda-boyama-telimati",
}

# Dəyişiklikləri tətbiq et
for old_url, new_url in replacements.items():
    content = content.replace(old_url, new_url)

# sitemap.xml faylını yenidən yaz
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ sitemap.xml uğurla yeniləndi!")
