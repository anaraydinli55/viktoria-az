# -*- coding: utf-8 -*-
# Viktoria AZ - Product JSON-LD yeniləyici (GitHub Actions + lokal istifadə)
import os, re, json, glob, copy, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BASE = 'https://viktoria-az.store'
TODAY = datetime.date.today()
VALID_UNTIL = '%d-12-31' % (TODAY.year + 1)
DEFAULT_PRICE = '5.00'
STOCK = 100
NO_STOCK = ('viktoria-sabitlesdirici-paltar-boyasi',)
EXTRA_PAGES = ['pitturafelice.html', 'sprey1.html']
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

DEST = {"@type": "DefinedRegion", "addressCountry": "AZ"}
DELIVERY = {"@type": "ShippingDeliveryTime",
            "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
            "transitTime": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 3, "unitCode": "DAY"}}
RETURN_POLICY = {"@type": "MerchantReturnPolicy", "applicableCountry": "AZ",
                 "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                 "merchantReturnDays": 14,
                 "returnMethod": "https://schema.org/ReturnByMail",
                 "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
                 "refundType": "https://schema.org/FullRefund",
                 "merchantReturnLink": BASE + "/iade-politikasi.html"}


def shipping_no_rate():
    # çatdırılma haqqı bilərəkdən yazılmır
    return {"@type": "OfferShippingDetails", "shippingDestination": copy.deepcopy(DEST),
            "deliveryTime": copy.deepcopy(DELIVERY)}


def rd(p):
    raw = open(p, encoding='utf-8', newline='').read()
    return raw.replace('\r\n', '\n'), ('\r\n' in raw)


def wr(p, t, crlf):
    if crlf:
        t = t.replace('\n', '\r\n')
    open(p, 'w', encoding='utf-8', newline='').write(t)


def money(v):
    try:
        return '%.2f' % float(str(v).replace(',', '.'))
    except Exception:
        return v


def edit_ld(t, fn):
    def sub(m):
        try:
            obj = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        before = json.dumps(obj, sort_keys=True, ensure_ascii=False)
        fn(obj)
        if json.dumps(obj, sort_keys=True, ensure_ascii=False) == before:
            return m.group(0)
        raw = m.group(2)
        first = next((l for l in raw.split('\n') if l.strip()), '')
        ind = first[:len(first) - len(first.lstrip())]
        tail = raw[raw.rfind('\n') + 1:]
        if tail.strip():
            tail = ''
        body = '\n'.join(ind + l for l in json.dumps(obj, ensure_ascii=False, indent=2).split('\n'))
        return m.group(1) + '\n' + body + '\n' + tail + m.group(3)
    return LD.sub(sub, t)


def enrich_offer(o, with_stock, shipping):
    if not isinstance(o, dict) or o.get('@type') != 'Offer':
        return
    if 'price' in o:
        o['price'] = money(o['price'])
    else:
        o['price'] = DEFAULT_PRICE
        o['priceCurrency'] = 'AZN'
    o.setdefault('availability', 'https://schema.org/InStock')
    if str(o.get('priceValidUntil', ''))[:10] < TODAY.isoformat():
        o['priceValidUntil'] = VALID_UNTIL
    o['hasMerchantReturnPolicy'] = copy.deepcopy(RETURN_POLICY)
    if shipping is not None:
        o['shippingDetails'] = shipping
    if with_stock:
        o['inventoryLevel'] = {"@type": "QuantitativeValue", "value": STOCK}


def enrich_product(obj, with_stock, shipping_fn=shipping_no_rate):
    if not isinstance(obj, dict) or obj.get('@type') != 'Product':
        return False
    obj.setdefault('brand', {"@type": "Brand", "name": "Viktoria"})
    offs = obj.get('offers')
    for o in (offs if isinstance(offs, list) else [offs]):
        enrich_offer(o, with_stock, shipping_fn() if shipping_fn else None)
    return True


def build_product(t, dirname):
    g = lambda pat: (re.search(pat, t, re.S) or [None, ''])[1].strip()
    h1 = re.sub(r'<[^>]+>', '', g(r'<h1[^>]*>(.*?)</h1>'))
    title = g(r'<title>(.*?)</title>')
    desc = g(r'<meta name="description" content="([^"]*)"')
    img = g(r'<meta property="og:image" content="([^"]*)"')
    url = g(r'rel="canonical" href="([^"]*)"') or (BASE + '/' + dirname)
    obj = {"@context": "https://schema.org", "@type": "Product", "name": h1 or title, "description": desc,
           "image": [img] if img else [], "brand": {"@type": "Brand", "name": "Viktoria"},
           "sku": "VIK-" + dirname.replace('viktoria-', '').replace('-paltar-boyasi', '').upper(),
           "offers": {"@type": "Offer", "url": url, "priceCurrency": "AZN", "price": DEFAULT_PRICE,
                      "availability": "https://schema.org/InStock",
                      "itemCondition": "https://schema.org/NewCondition"}}
    if not obj['image']:
        del obj['image']
    return obj


def process(path, color):
    t, crlf = rd(path)
    dirname = os.path.dirname(path)
    with_stock = color and dirname not in NO_STOCK
    found = []

    def fn(o):
        if enrich_product(o, with_stock):
            found.append(1)
    new = edit_ld(t, fn)
    if not found and color:
        o = build_product(t, dirname)
        enrich_product(o, with_stock)
        block = '  <script type="application/ld+json">\n' + '\n'.join(
            '    ' + l for l in json.dumps(o, ensure_ascii=False, indent=2).split('\n')) + '\n  </script>\n'
        new = new.replace('</head>', block + '</head>', 1)
        found.append(1)
    if new != t:
        wr(path, new, crlf)
        return True
    return False


def main():
    os.chdir(ROOT)
    color = sorted(glob.glob('viktoria-*-paltar-boyasi/index.html'))
    n = 0
    for p in color:
        n += process(p, True)
    for p in EXTRA_PAGES:
        if os.path.isfile(p):
            n += process(p, False)
    print('Product schema: %d səhifə yeniləndi (%d rəng səhifəsi yoxlandı)' % (n, len(color)))


if __name__ == '__main__':
    main()
