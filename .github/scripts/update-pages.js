const fs = require('fs');
const path = require('path');

const productsAz = [ ["Qara", "viktoria-qara-paltar-boyasi"], ["Tünd Göy", "viktoria-tund-goy-paltar-boyasi"], ["Gül Qurusu", "viktoria-gul-qurusu-paltar-boyasi"], /* Digər 57 rəngi bura əlavə edin */ ];
const productsRu = [ ["Чёрный", "ru/viktoria-chernaya-kraska-dlya-odejdy"], ["Пыльная роза", "ru/viktoria-pylnaya-roza-kraska-dlya-odejdy"], /* Digər 58 rəngi bura əlavə edin */ ];

const templates = {
    az: {
        titles: ["[color] Rəngli Paltar Boyası - Evdə Boyama üçün Viktoria", "Viktoria [color] Rəngli Paltar Boyası - 5 AZN", "Paltarları [color] Rəngə Boyamaq üçün Viktoria Boyası"],
        descriptions: ["[color] rəngli Viktoria boyası ilə evdə paltar boyamaq çox asandır.", "Geyiminizə yeni həyat vermək üçün [color] tonu ən ideal seçimdir.", "Solmuş paltarlarınızı [color] rənginin parlaqlığı ilə yenidən canlandırın."],
        intros: ["Viktoria [color] boyası pambıq və kətan parçalarda mükəmməl nəticə verir.", "[color] tonu tekstil məhsullarınız üçün modern bir görünüş təmin edir.", "Bu boya parçanın teksturasını pozmadan dərindən nüfuz edir."]
    },
    ru: {
        titles: ["Краска для одежды [color] - Viktoria купить в Баку", "Viktoria краска цвета [color] - 5 AZN", "Профессиональное окрашивание в цвет [color] дома"],
        descriptions: ["Восстановите яркость ваших вещей с помощью красителя цвета [color].", "Краска Viktoria цвета [color] идеально подходит для натуральных тканей.", "Оживите свою одежду с помощью качественной краски Viktoria цвета [color]."],
        intros: ["Этот краситель идеально ложится на хлопок, лен и вискозу.", "Оттенок [color] от Viktoria придает вашим вещам благородный и современный вид.", "Глубоко проникает в волокна, обеспечивая стойкий цвет [color]."]
    }
};

function updateFile(filePath, lang, color, index) {
    if (!fs.existsSync(filePath)) {
        console.log(`Fayl tapılmadı: ${filePath}`);
        return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    const t = templates[lang];

    // Unikal dataları seçirik
    const title = t.titles[index % t.titles.length].replace("[color]", color);
    const desc = t.descriptions[index % t.descriptions.length].replace("[color]", color);
    const intro = t.intros[index % t.intros.length].replace("[color]", color);

    // HTML daxilində dəyişikliklər (Regex ilə)
    content = content.replace(/<title>.*?<\/title>/i, `<title>${title}</title>`);
    content = content.replace(/<meta\s+name="description"\s+content=".*?"/i, `<meta name="description" content="${desc}"`);
    content = content.replace(/<h1>.*?<\/h1>/i, `<h1>${title}</h1>`);
    
    // Əgər səhifədə xüsusi bir yer varsa (məsələn p teqi), onu da dəyişə bilərik:
    // Bu hissə səhifədəki ilk <p> teqini unikal intro ilə əvəz edir
    content = content.replace(/<p>.*?<\/p>/i, `<p>${intro}</p>`);

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Yeniləndi: ${filePath}`);
}

// AZ Fayllarını yenilə
productsAz.forEach((p, i) => {
    const filePath = path.join(__dirname, '..', `${p[1]}.html`);
    updateFile(filePath, 'az', p[0], i);
});

// RU Fayllarını yenilə
productsRu.forEach((p, i) => {
    const filePath = path.join(__dirname, '..', `${p[1]}.html`);
    updateFile(filePath, 'ru', p[0], i);
});
