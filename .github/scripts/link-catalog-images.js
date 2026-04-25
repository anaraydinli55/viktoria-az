/**
 * link-catalog-images.js  (v4)
 *
 * AZ: /viktoria-*-paltar-boyasi/   →  catalog/index.html
 * RU: /ru/viktoria-*-odejdy/       →  ru/catalog/index.html
 *
 * Məntiq:
 *   1. Hər dil üçün product qovluqlarını tara → sekil_adi → URL xəritəsi qur
 *   2. Uyğun catalog/index.html-i aç:
 *        - Mövcud <a> tapılırsa  → href-i yenilə
 *        - <a> yoxdursa          → yeni <a> ilə sar
 *   3. Dəyişdirilmiş faylı geri yaz
 */

const fs   = require('fs');
const path = require('path');

let cheerio;
try {
  cheerio = require('cheerio');
} catch {
  console.error('cheerio tapilmadi. Evvelce: npm install cheerio');
  process.exit(1);
}

const ROOT = process.cwd();

// ─────────────────────────────────────────────────────────────────────────────
// Köməkçi: scanDir içindəki qovluqları gəz, keyword ilə uyğunları tap
// urlPrefix — hər URL-ə əlavə olunacaq ön şəkilçi
// ─────────────────────────────────────────────────────────────────────────────
function buildProductMap(scanDir, urlPrefix, keyword) {
  const map = {};

  if (!fs.existsSync(scanDir)) {
    console.warn(`  [!] Qovluq tapilmadi: ${scanDir}`);
    return map;
  }

  const entries = fs.readdirSync(scanDir, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (!entry.name.includes(keyword)) continue;

    const indexFile = path.join(scanDir, entry.name, 'index.html');
    if (!fs.existsSync(indexFile)) continue;

    const html = fs.readFileSync(indexFile, 'utf-8');
    const $p   = cheerio.load(html);

    $p('img[src]').each((_i, el) => {
      const src = $p(el).attr('src');
      if (!src) return;
      const filename = path.basename(src);
      if (!filename.endsWith('.webp')) return;
      if (!map[filename]) {
        map[filename] = urlPrefix + '/' + entry.name;
        console.log(`    ${filename}  -->  ${map[filename]}`);
      }
    });
  }

  return map;
}

// ─────────────────────────────────────────────────────────────────────────────
// Köməkçi: catalog faylını xəritəyə əsasən yenilə
// ─────────────────────────────────────────────────────────────────────────────
function processCatalog(catalogFile, productMap, label) {
 console.log(`\n  [${label}] ${catalogFile} islenilir...`);

  if (!fs.existsSync(catalogFile)) {
    console.warn(`  [!] Fayl tapilmadi: ${catalogFile}`);
    return;
  }

  const html = fs.readFileSync(catalogFile, 'utf-8');
  const $c   = cheerio.load(html, { decodeEntities: false });

  let updated  = 0;
  let wrapped  = 0;
  let notFound = 0;

  $c('img[src]').each((_i, el) => {
    const src = $c(el).attr('src');
    if (!src || !src.endsWith('.webp')) return;

    const filename   = path.basename(src);
    const productUrl = productMap[filename];

    if (!productUrl) {
      console.warn(`    Uygunluq yoxdur: ${filename}`);
      notFound++;
      return;
    }

    const $existingLink = $c(el).closest('a');

    if ($existingLink.length > 0) {
      const oldHref = $existingLink.attr('href') || '(yox)';
      $existingLink.attr('href', productUrl);
      console.log(`    Yenilendi: ${filename}`);
      console.log(`      kohne: ${oldHref}`);
      console.log(`      yeni : ${productUrl}`);
      updated++;
    } else {
      $c(el).wrap(<a href="${productUrl}" style="display:contents;"></a>);
      console.log(`    Sarildi: ${filename}  -->  ${productUrl}`);
      wrapped++;
    }
  });

  fs.writeFileSync(catalogFile, $c.html(), 'utf-8');

  console.log(`  [${label}] Netice: yenilendi=${updated} | sarildi=${wrapped} | tapilmadi=${notFound}`);
}

// ─────────────────────────────────────────────────────────────────────────────
// AZ — kök qovluq, keyword: paltar-boyasi
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n========== AZ: Product xeritesi ==========');
const azMap = buildProductMap(ROOT, '', 'paltar-boyasi');
processCatalog(path.join(ROOT, 'catalog', 'index.html'), azMap, 'AZ');

// ─────────────────────────────────────────────────────────────────────────────
// RU — ru/ alt qovluğu, keyword: odejdy
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n========== RU: Product xeritesi ==========');
const ruMap = buildProductMap(path.join(ROOT, 'ru'), '/ru', 'odejdy');
processCatalog(path.join(ROOT, 'ru', 'catalog', 'index.html'), ruMap, 'RU');

console.log('\n================================================');
console.log('  Her iki catalog ugurla yenilendi!');
console.log('================================================\n');
