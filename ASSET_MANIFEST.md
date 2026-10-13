# Luminex Asset Manifest

This document records all photography, vector graphics, and brand assets used within the Luminex storefront, their license/permission status, dimensions, central mapping, and intended use.

## Asset Licensing & Origin Policy
In accordance with fair usage and intellectual property compliance:
- No proprietary Apple assets, logos, or copyrighted promotional photography are scraped, mirrored, or downloaded.
- All product assets and brand elements are original, high-precision SVG vector illustrations created specifically for the Luminex brand identity, inspired by modern industrial electronics design.
- All assets are resolution-independent (scalable vector graphics), avoiding pixelation and excessive bandwidth consumption.

---

## 1. Product Illustrations

| Asset Name | Relative Path | Format | ViewBox / Dims | License Status | Intended Use | Associated Product SKU / Name |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Luminex Pro 15 | `products/luminex_pro_15.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Store Hero, Latest Carousel, Detail View | Flagship triple-camera titanium smartphone |
| Luminex Air 15 | `products/luminex_air_15.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Latest Carousel, Product Grid | Dual-camera slim pastel smartphone |
| Luminex Mini 15 | `products/luminex_mini_15.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Catalog & Category View | Compact flagship smartphone |
| Luminex Book Pro 16 | `products/luminex_book_pro_16.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Store Hero 2, Latest Carousel, Detail View | Space Black pro laptop with Liquid Retina display |
| Luminex Book Air 15 | `products/luminex_book_air_15.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Laptop Category & Catalog Grid | Ultra-thin consumer aluminum laptop |
| Luminex Buds Pro 3 | `products/luminex_buds_pro_3.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Audio Showcase, Latest Carousel | Noise cancelling earbuds in wireless charging case |
| Luminex Phones Max | `products/luminex_phones_max.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Audio Category & Detail View | Premium aluminum over-ear headphones |
| Luminex Watch Ultra 2 | `products/luminex_watch_ultra_2.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Latest Carousel, Wearables Category | Titanium rugged adventure smartwatch |
| Luminex Watch Series 9 | `products/luminex_watch_series_9.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Wearables Grid & Detail View | Slim curved bezel everyday smartwatch |
| Luminex Pad Pro 13" | `products/luminex_pad_pro_13.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Latest Carousel, Tablets Category | Ultra-thin OLED display tablet with docked stylus |
| Luminex MagCharge 30W | `products/luminex_magcharge.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Accessories Category & Detail View | Magnetic fast charging aluminum puck |
| Luminex Smart Folio | `products/luminex_smart_folio.svg` | SVG | 500 × 500 | Proprietary (Original Luminex Asset) | Accessories Category & Detail View | Folding soft-touch protective tablet case |

---

## 2. Category Navigation Icons

| Asset Name | Relative Path | Format | ViewBox / Dims | License Status | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Smartphones Icon | `categories/cat_smartphones.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |
| Laptops Icon | `categories/cat_laptops.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |
| Audio Icon | `categories/cat_audio.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |
| Wearables Icon | `categories/cat_wearables.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |
| Tablets Icon | `categories/cat_tablets.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |
| Accessories Icon | `categories/cat_accessories.svg` | SVG | 120 × 120 | Proprietary (Original Luminex Asset) | Horizontal Store Category Bar |

---

## 3. Brand & Campaign Motifs

| Asset Name | Relative Path | Format | ViewBox / Dims | License Status | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Festive Mandala Motif | `brand/mandala_accent.svg` | SVG | 600 × 600 | Proprietary (Original Luminex Asset) | Festive Store Header Artwork & Editorial Card Background |

---

## 4. Central Product Image Mapping
Central mapping is defined in `store/management/commands/attach_assets.py` and stored in the Django database fields (`Product.main_image` and `Category.image`), allowing database-driven changes without altering HTML templates.
