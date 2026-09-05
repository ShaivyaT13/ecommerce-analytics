# E-Commerce Data Findings

I looked at roughly 20,000 cleaned orders from January 2024 to June 2025. This covered 500 customers buying 28 products across 5 categories in 4 regions. Here's what the data showed.

## The Big Picture

| Metric | Value |
|---|---|
| Revenue | ₹6,018,372 |
| Profit | ₹1,434,337 |
| Margin | 23.8% |
| Orders | 19,940 |
| Customers | 500 |
| Avg Order Value | ₹301.82 |

## Revenue by category

| Category | Revenue | Profit | Avg Margin |
|---|---|---|---|
| Electronics | ₹3,756,805 | ₹703,301 | 31.2% |
| Furniture | ₹1,552,920 | ₹411,160 | 27.1% |
| Clothing | ₹433,518 | ₹190,414 | 45.6% |
| Food & Beverages | ₹142,826 | ₹60,483 | 42.4% |
| Office Supplies | ₹132,304 | ₹68,980 | 55.9% |

Electronics brings in most of the money (62.4% of total revenue) but has pretty mediocre margins at 31.2%. Interestingly, Office Supplies makes the least revenue but kills it on margins at 55.9%, almost double that of Electronics.

## Highest profit margins

1. Office Supplies — 55.9%
2. Clothing — 45.6%
3. Food & Beverages — 42.4%
4. Electronics — 31.2%
5. Furniture — 27.1%

There's a clear flip here: the categories bringing in less cash are actually the most profitable per item. The high-volume Electronics are likely getting discounted heavily to move units.

## Regional breakdown

| Region | Revenue | Profit | Customers | Avg Margin |
|---|---|---|---|---|
| North | ₹1,583,332 | ₹376,873 | 128 | 39.7% |
| West | ₹1,552,485 | ₹370,829 | 130 | 39.6% |
| East | ₹1,494,442 | ₹353,671 | 129 | 39.4% |
| South | ₹1,375,583 | ₹329,611 | 113 | 39.1% |

Things are pretty even across the board, with North slightly in the lead. The South region has the fewest customers and lowest revenue, so there might be room to grow there. Margins are basically identical everywhere.

## Top 10 products

| Product | Units Sold | Revenue | Profit |
|---|---|---|---|
| Laptop | 1,920 | ₹1,412,640 | ₹164,640 |
| Smartphone | 1,845 | ₹861,000 | ₹159,900 |
| Tablet | 1,934 | ₹635,198 | ₹132,358 |
| Standing Desk | 1,816 | ₹595,630 | ₹141,630 |
| Monitor | 1,999 | ₹559,185 | ₹119,405 |
| Desk | 1,726 | ₹320,760 | ₹79,120 |
| Office Chair | 1,839 | ₹255,968 | ₹72,068 |
| Bookshelf | 1,911 | ₹214,278 | ₹61,398 |
| Filing Cabinet | 1,988 | ₹166,284 | ₹56,944 |
| Jacket | 1,945 | ₹145,448 | ₹57,923 |

Laptops alone are almost a quarter of all revenue (23.5%). If you look at just the top 3 items (all tech), they make up nearly half the money coming in.

## High volume, low profit products

| Product | Units | Revenue | Profit | Margin |
|---|---|---|---|---|
| Laptop | 1,920 | ₹1,412,640 | ₹164,640 | 11.0% |
| Smartphone | 1,845 | ₹861,000 | ₹159,900 | 17.7% |
| Tablet | 1,934 | ₹635,198 | ₹132,358 | 19.9% |
| Monitor | 1,999 | ₹559,185 | ₹119,405 | 20.3% |
| Standing Desk | 1,816 | ₹595,630 | ₹141,630 | 22.5% |

Laptops only have an 11% margin, which is super low considering how much revenue they drive. We're probably discounting them too much or the base cost is just too high. Definitely something to look into.

## Customer habits

All 500 customers in this dataset bought more than once (expected since it's synthetic data spanning 18 months, but good to note). 

When breaking down spend:

| Segment | Customers | Revenue | Profit |
|---|---|---|---|
| High Value (≥ ₹5,000) | 486 | ₹5,958,795 | ₹1,415,573 |
| Medium Value (₹2,000–₹4,999) | 14 | ₹59,576 | ₹18,763 |

Almost everyone (97.2%) falls into the High Value bucket. There are just 14 people in the Medium tier who we could probably bump up with a targeted promo.

## Month-to-month trends

| Month | Revenue | Profit |
|---|---|---|
| 2024-01 | ₹328,098 | ₹75,702 |
| 2024-03 | ₹398,739 | ₹96,755 |
| 2024-06 | ₹325,205 | ₹75,628 |
| 2024-09 | ₹341,994 | ₹78,920 |
| 2024-12 | ₹313,257 | ₹76,465 |
| 2025-03 | ₹353,366 | ₹85,330 |
| 2025-06 | ₹351,514 | ₹85,687 |

Things are pretty steady. Revenue bounces around between ₹294K and ₹399K without any crazy spikes or drops. March 2024 was the best month, but overall it's just consistent.

## How people pay

| Method | Orders | Revenue |
|---|---|---|
| UPI | 5,981 | ₹1,801,180 |
| Credit Card | 5,882 | ₹1,758,467 |
| Debit Card | 4,067 | ₹1,247,445 |
| Cash | 2,050 | ₹653,750 |
| Net Banking | 1,960 | ₹557,530 |

UPI and Credit Cards are king here, making up about 59% of orders. Almost 90% of all transactions are digital, so people are definitely comfortable paying online.

## Takeaways

- **Fix laptop pricing:** An 11% margin on our biggest seller is dragging down the whole average (which is normally ~24%). Getting even a slightly better margin here would be a massive win.
- **Push into the South:** It's lagging behind the other regions in customer count and revenue. Might need a targeted ad push.
- **Sell more Office Supplies and Clothes:** The margins here are great (56% and 46%). If we can increase the volume on these, profits will jump.
- **Run a UPI promo:** Since everyone is already using it, a small UPI cashback offer could drive even more sales.
