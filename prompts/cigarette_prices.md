Extract cigarette prices from this page of The Smokers' Handbook.

Rules:
- Extract cigarettes only.
- Ignore tobacco, cigars, snuff, adverts, addresses, phone numbers, and "prices on application".
- Extract only packet sizes 10 and 20.
- Preserve prices exactly as printed.
- Use null if a 10 or 20 price is absent.
- If a price is printed as "20 for 3/6", record pack_20 as "3/6".
- If a price is printed as "10 for 1/9", record pack_10 as "1/9".
- Do not include "for 10" or "for 20" inside the price field.
- Return JSON only.

Return a list of objects with exactly these fields:
manufacturer_or_distributor
product
pack_10
pack_20
notes