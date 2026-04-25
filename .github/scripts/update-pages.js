
const fs = require('fs');
const path = require('path');

// --- 120 RƏNGİN TAM SİYAHISI ---
const productsAz = [
    ["Qara", "viktoria-qara-paltar-boyasi"], ["Tünd Göy", "viktoria-tund-goy-paltar-boyasi"], ["Qırmızı", "viktoria-qirmizi-paltar-boyasi"], ["Yaşıl", "viktoria-yasil-paltar-boyasi"], ["Sarı", "viktoria-sari-paltar-boyasi"], ["Tünd Mavi", "viktoria-tund-mavi-paltar-boyasi"], ["Qəhvəyi", "viktoria-qehveyi-paltar-boyasi"], ["Tünd Qəhvəyi", "viktoria-tund-qehveyi-paltar-boyasi"], ["Çəhrayı", "viktoria-cehrayi-paltar-boyasi"], ["Açıq Mavi", "viktoria-aciq-mavi-paltar-boyasi"], ["Orta Qəhvəyi", "viktoria-orta-qehveyi-paltar-boyasi"], ["Açıq Göy", "viktoria-aciq-goy-paltar-boyasi"], ["Orta Mavi", "viktoria-orta-mavi-paltar-boyasi"], ["Gül Qurusu", "viktoria-gul-qurusu-paltar-boyasi"], ["Bej", "viktoria-bej-paltar-boyasi"], ["Tünd Boz", "viktoria-tund-boz-paltar-boyasi"], ["Xaki", "viktoria-xaki-paltar-boyasi"], ["Açıq Bənövşəyi", "viktoria-aciq-mor-paltar-boyasi"], ["Bordovu", "viktoria-bordoviy-paltar-boyasi"], ["Yanıq Qəhvəyi", "viktoria-yaniq-qehveyi-paltar-boyasi"], ["Narıncı", "viktoria-narinci-paltar-boyasi"], ["Güvəz", "viktoria-guvez-paltar-boyasi"], ["Yemiş Rəngi", "viktoria-yemis-rengi-paltar-boyasi"], ["Buz Mavisi", "viktoria-buz-mavisi-paltar-boyasi"], ["Şaftalı", "viktoria-yavruagzi-paltar-boyasi"], ["Tünd Çəhrayı", "viktoria-tund-cehrayi-paltar-boyasi"], ["Al Qırmızı", "viktoria-al-qirmizi-paltar-boyasi"], ["Atəşi Çəhrayı", "viktoria-atesi-cehrayi-paltar-boyasi"], ["Nar Çiçəyi", "viktoria-nar-ciceyi-paltar-boyasi"], ["Tünd Qırmızı", "viktoria-tund-qirmizi-paltar-boyasi"], ["Gilas Rəngi", "viktoria-visne-curuyu-paltar-boyasi"], ["Açıq Bej", "viktoria-aciq-bej-paltar-boyasi"], ["Tütün Rəngi", "viktoria-tutun-rengi-paltar-boyasi"], ["Tünd Bənövşəyi", "viktoria-tund-mor-paltar-boyasi"], ["Lavanda", "viktoria-eflatun-paltar-boyasi"], ["Açıq Boz", "viktoria-aciq-boz-paltar-boyasi"], ["Dəniz Dalğası", "viktoria-cam-gobeyi-paltar-boyasi"], ["Marsala", "viktoria-serabi-paltar-boyasi"], ["Açıq Salat", "viktoria-filizi-aciq-paltar-boyasi"], ["Nefti Rəngi", "viktoria-nefti-rengi-paltar-boyasi"], ["Kanarya", "viktoria-kanarya-paltar-boyasi"], ["Portağal", "viktoria-portagal-paltar-boyasi"], ["Zümrüd", "viktoria-zumrud-paltar-boyasi"], ["Petrol", "viktoria-petrol-paltar-boyasi"], ["Zeytuni", "viktoria-zeytuni-paltar-boyasi"], ["İndiqo", "viktoria-civit-mavi-paltar-boyasi"], ["Göy Bənövşəyi", "viktoria-mor-goy-paltar-boyasi"], ["Tünd Marsala", "viktoria-tund-serabi-paltar-boyasi"], ["Tünd Lavanda", "viktoria-tund-eflatun-paltar-boyasi"], ["Bənövşəyi", "viktoria-benovseyi-paltar-boyasi"], ["Qızılı Sarı", "viktoria-qizili-sari-paltar-boyasi"], ["Tünd Sarı", "viktoria-tund-sari-paltar-boyasi"], ["Cins Mavisi", "viktoria-cins-mavisi-paltar-boyasi"], ["Orta Göy", "viktoria-orta-goy-paltar-boyasi"], ["Firuzəyi", "viktoria-firuzeyi-paltar-boyasi"], ["Tünd Bej", "viktoria-tund-bej-paltar-boyasi"], ["Açıq Qəhvəyi", "viktoria-aciq-qehveyi-paltar-boyasi"], ["Tünd Yaşıl", "viktoria-tund-yasil-paltar-boyasi"], ["Tünd Salat", "viktoria-tund-filizi-paltar-boyasi"], ["Sabitləyici", "viktoria-sabitlesdirici-paltar-boyasi"]
];

const productsRu = [
    ["Чёрный", "ru/viktoria-chernaya-kraska-dlya-odejdy"], ["Тёмно-синий", "ru/viktoria-temno-sinyaya-kraska-dlya-odejdy"], ["Красный", "ru/viktoria-krasnaya-kraska-dlya-odejdy"], ["Зелёный", "ru/viktoria-zelenaya-kraska-dlya-odejdy"], ["Жёлтый", "ru/viktoria-jeltaya-kraska-dlya-odejdy"], ["Тёмно-голубой", "ru/viktoria-temno-golubaya-kraska-dlya-odejdy"], ["Коричневый", "ru/viktoria-korichnevaya-kraska-dlya-odejdy"], ["Тёмно-коричневый", "ru/viktoria-temno-korichnevaya-kraska-dlya-odejdy"], ["Розовый", "ru/viktoria-rozovaya-kraska-dlya-odejdy"], ["Светло-голубой", "ru/viktoria-golubaya-kraska-dlya-odejdy"], ["Средне-коричневый", "ru/viktoria-sredne-korichnevaya-kraska-dlya-odejdy"], ["Светло-синий", "ru/viktoria-golubaia-kraska-dlya-odejdy"], ["Средне-голубой", "ru/viktoria-sredne-sinyaya-kraska-dlya-odejdy"], ["Пыльная роза", "ru/viktoria-pylnaya-roza-kraska-dlya-odejdy"], ["Бежевый", "ru/viktoria-bejeviy-kraska-dlya-odejdy"], ["Тёмно-серый", "ru/viktoria-temno-seraya-kraska-dlya-odejdy"], ["Хаки", "ru/viktoria-haki-kraska-dlya-odejdy"], ["Светло-фиолетовый", "ru/viktoria-svetlo-fioletovaya-kraska-dlya-odejdy"], ["Бордовый", "ru/viktoria-bordovaya-kraska-dlya-odejdy"], ["Жжёный коричневый", "ru/viktoria-jjenniy-korichneviy-kraska-dlya-odejdy"], ["Оранжевый", "ru/viktoria-oranjevaya-kraska-dlya-odejdy"], ["Бордово-красный", "ru/viktoria-bordoviy-ksrasniy-kraska-dlya-odejdy"], ["Дынный цвет", "ru/viktoria-dynniy-kraska-dlya-odejdy"], ["Ледяной голубой", "ru/viktoria-ledyanoy-goluboy-kraska-dlya-odejdy"], ["Персиковый", "ru/viktoria-persikoviy-kraska-dlya-odejdy"], ["Тёмно-розовый", "ru/viktoria-temno-rozovaya-kraska-dlya-odejdy"], ["Ярко-красный", "ru/viktoria-aliy-krasniy-kraska-dlya-odejdy"], ["Огненно-розовый", "ru/viktoria-ognenno-rozovaya-kraska-dlya-odejdy"], ["Цветок граната", "ru/viktoria-tsvetok-granata-kraska-dlya-odejdy"], ["Тёмно-красный", "ru/viktoria-temno-krasniy-kraska-dlya-odejdy"], ["Спелая вишня", "ru/viktoria-vyshnevo-krasniy-kraska-dlya-odejdy"], ["Светло бежевый", "ru/viktoria-svetlo-bejeviy-kraska-dlya-odejdy"], ["Табачный", "ru/viktoria-tabachniy-kraska-dlya-odejdy"], ["Тёмно-фиолетовый", "ru/viktoria-temno-fioletovaya-kraska-dlya-odejdy"], ["Лавандовый", "ru/viktoria-purpurniy-kraska-dlya-odejdy"], ["Светло-серый", "ru/viktoria-svetlo-seraya-kraska-dlya-odejdy"], ["Морская волна", "ru/viktoria-tsvet-morskoj-volny-kraska-dlya-odejdy"], ["Марсала", "ru/viktoria-marsala-kraska-dlya-odejdy"], ["Светло-салатовый", "ru/viktoria-svetlo-salatoviy-kraska-dlya-odejdy"], ["Нефтяной", "ru/viktoria-neftyanoy-kraska-dlya-odejdy"], ["Канареечный", "ru/viktoria-kanareechniy-kraska-dlya-odejdy"], ["Апельсиновый", "ru/viktoria-apelsinoviy-kraska-dlya-odejdy"], ["Изумрудный", "ru/viktoria-izumrudniy-kraska-dlya-odejdy"], ["Петроль", "ru/viktoria-petrol-kraska-dlya-odejdy"], ["Оливковый", "ru/viktoria-olivkoviy-kraska-dlya-odejdy"], ["Индиго", "ru/viktoria-indigo-kraska-dlya-odejdy"], ["Сине-фиолетовый", "ru/viktoria-sine-fioletovaya-kraska-dlya-odejdy"], ["Темная Марсала", "ru/viktoria-temnaya-marsala-kraska-dlya-odejdy"], ["Тёмная лаванда", "ru/viktoria-temno-purpurniy-lavanda-kraska-dlya-odejdy"], ["Фиолетовый", "ru/viktoria-fioletovaya-kraska-dlya-odejdy"], ["Золотисто-жёлтый", "ru/viktoria-zolotisto-jeltaya-kraska-dlya-odejdy"], ["Тёмно-жёлтый", "ru/viktoria-temno-jeltaya-kraska-dlya-odejdy"], ["Джинсовый", "ru/viktoria-dzhinsovyy-siniy-kraska-dlya-odezhdy"], ["Средне-синий", "ru/viktoria-sredne-siniy-kraska-dlya-odezhdy"], ["Бирюзовый", "ru/viktoria-biryuzovaya-kraska-dlya-odezhdy"], ["Темно-бежевый", "ru/viktoria-temno-bej-kraska-dlya-odezhdy"], ["Светло-коричневый", "ru/viktoria-svetlo-korichnevaya-kraska-dlya-odezhdy"], ["Темно-Зелёный", "ru/viktoria-temno-zelyonaya-kraska-dlya-odezhdy"], ["Темно-салатовый", "ru/viktoria-temno-salatoviy-kraska-dlya-odezhdy"], ["Фиксатор", "ru/viktoria-zakrepitel-cveta-kraski-dlya-odezhdy"]
];

const templates = {
    az: {
        titles: ["[color] Rəngli Paltar Boyası – 5 AZN | Viktoria AZ", "Viktoria [color] Rəngli Paltar Boyası - Sifariş Et", "[color] Paltar Boyası Sifarişi – Bakı və Azərbaycan"],
        descriptions: ["Solmuş geyimlərinizi Viktoria [color] paltar boyası ilə yenidən canlandırın. Qiymət: 5 AZN.", "Geyiminizə yeni həyat bəxş etmək üçün [color] tonu ideal seçimdir. WhatsApp ilə sifariş.", "[color] rənginin parlaqlığı ilə solmuş paltarlarınızı asanlıqla bərpa edin. Çatdırılma var."],
        intros: ["solmuş, rəngi açılmış və köhnəlmiş geyimləri yeniləmək üçün ideal seçimdir.", "geyimlərinizə modern və təravətli bir görünüş bəxş etmək üçün nəzərdə tutulub.", "tekstil məhsullarınızın rəngini peşəkar səviyyədə bərpa etməyə imkan verir."]
    },
    ru: {
        titles: ["Краска для одежды Viktoria — [color] за 5 AZN", "Купить краску Viktoria цвета [color] — Баку", "Профессиональный краситель Viktoria цвета [color]"],
        descriptions: ["Обновите выцветшую одежду с помощью краски Viktoria цвета [color]. Цена: 5 AZN.", "Краситель цвета [color] идеально подходит для хлопка и льна. Быстрая доставка.", "Верните яркость вашим вещам с помощью краски Viktoria оттенка [color]."],
        intros: ["идеальное решение для восстановления выцветших вещей или придания им нового оттенка.", "позволяет вернуть жизнь вашим любимым вещам всего за один цикл окрашивания.", "обеспечивает глубокое проникновение в волокна ткани и стойкий результат."]
    }
};

function updateFile(filePath, lang, color, slug, index) {
    if (!fs.existsSync(filePath)) return;

    let content = fs.readFileSync(filePath, 'utf8');
    const t = templates[lang];

    const title = t.titles[index % t.titles.length].replace("[color]", color);
    const desc = t.descriptions[index % t.descriptions.length].replace("[color]", color);
    const introText = t.intros[index % t.intros.length].replace("[color]", color);

    // 1. Title & Meta
    content = content.replace(/<title>.*?<\/title>/i, `<title>${title}</title>`);
    content = content.replace(/<meta\s+name="description"\s+content=".*?"/i, `<meta name="description" content="${desc}"`);
    
    // 2. Canonical & OG
    content = content.replace(/<link\s+rel="canonical"\s+href=".*?"/i, `<link rel="canonical" href="https://viktoria-az.store/${slug}"`);
    content = content.replace(/property="og:title"\s+content=".*?"/i, `property="og:title" content="${title}"`);
    content = content.replace(/property="og:description"\s+content=".*?"/i, `property="og:description" content="${desc}"`);
    content = content.replace(/property="og:url"\s+content=".*?"/i, `property="og:url" content="https://viktoria-az.store/${slug}"`);

    // 3. H1 & Intro P (Sizin xüsusi strukturunuz)
    content = content.replace(/<h1>.*?<\/h1>/i, `<h1>Viktoria ${color} Paltar Boyası</h1>`);
    
    // Intro P teqini hədəf alan Regex
    const introRegex = /(<div class="product-info">[\s\S]*?<p>)([\s\S]*?)(<\/p>)/i;
    const newIntroHtml = `$1\n            <strong>Viktoria ${color.toLowerCase()} paltar boyası</strong> ${introText}\n          $3`;
    content = content.replace(introRegex, newIntroHtml);

    // 4. JSON-LD Sxemaları (Product & Breadcrumb)
    content = content.replace(/"name":\s*"Viktoria.*?Boyası"/gi, `"name": "Viktoria ${color} Paltar Boyası"`);
    content = content.replace(/"url":\s*"https:\/\/viktoria-az.store\/viktoria-.*?"/gi, `"url": "https://viktoria-az.store/${slug}"`);

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Yeniləndi: ${filePath}`);
}

// BÜTÜN AZ SƏHİFƏLƏRİ
productsAz.forEach((p, i) => {
    const filePath = path.join(__dirname, '..', p[1], 'index.html');
    updateFile(filePath, 'az', p[0], p[1], i);
});

// BÜTÜN RU SƏHİFƏLƏRİ
productsRu.forEach((p, i) => {
    const filePath = path.join(__dirname, '..', p[1], 'index.html');
    updateFile(filePath, 'ru', p[0], p[1], i);
});
