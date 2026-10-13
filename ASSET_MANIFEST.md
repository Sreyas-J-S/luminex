# Luminex Asset Manifest

This document records all photography, vector graphics, and brand assets used within the Luminex storefront, their license/permission status, dimensions, central mapping, and intended use.

## Asset Licensing & Origin Policy
In accordance with fair usage and intellectual property compliance:
- No proprietary Apple assets, logos, or copyrighted promotional photography are scraped, mirrored, or downloaded.
- All product assets and brand elements are original, high-precision SVG vector illustrations created specifically for the Luminex brand identity, inspired by modern industrial electronics design.
- All assets are resolution-independent (scalable vector graphics), avoiding pixelation and excessive bandwidth consumption.

---

## 1. Photorealistic Product Photography

All product photography consists of high-resolution, commercial e-commerce studio shots (1:1 square ratio, 1024 × 1024) featuring realistic metallic finishes, precise glass reflections, natural lighting, and soft ground contact shadows on pure white seamless backgrounds.

| Asset Name | Relative Path | Format | Dims | License / Origin | Intended Use | Associated Product SKU / Name |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Luminex Pro 15 | `products/luminex_pro_15.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Store Hero, Latest Carousel, Detail View | Flagship triple-camera natural titanium smartphone |
| Luminex Air 15 | `products/luminex_air_15.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Latest Carousel, Product Grid, Trade-in | Dual-camera slim pastel smartphone |
| Luminex Mini 15 | `products/luminex_mini_15.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Catalog & Category View | Compact flagship smartphone |
| Luminex Book Pro 16 | `products/luminex_book_pro_16.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Store Hero 2, Latest Carousel, Detail View | Space Black pro laptop with Liquid Retina display |
| Luminex Book Air 15 | `products/luminex_book_air_15.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Laptop Category & Catalog Grid | Ultra-thin consumer aluminum laptop |
| Luminex Buds Pro 3 | `products/luminex_buds_pro_3.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Audio Showcase, Latest Carousel | Noise cancelling earbuds in wireless charging case |
| Luminex Phones Max | `products/luminex_phones_max.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Audio Category & Detail View | Premium aluminum over-ear headphones |
| Luminex Watch Ultra 2 | `products/luminex_watch_ultra_2.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Latest Carousel, Wearables Category | Titanium rugged adventure smartwatch |
| Luminex Watch Series 9 | `products/luminex_watch_series_9.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Wearables Grid & Detail View | Slim curved bezel everyday smartwatch |
| Luminex Pad Pro 13" | `products/luminex_pad_pro_13.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Latest Carousel, Tablets Category | Ultra-thin OLED display tablet with docked stylus |
| Luminex MagCharge 30W | `products/luminex_magcharge_30w.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Accessories Category & Detail View | Magnetic fast charging aluminum puck |
| Luminex Smart Folio | `products/luminex_smart_folio.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Accessories Category & Detail View | Folding soft-touch protective tablet case |

---

## 2. Category Navigation Badges

| Asset Name | Relative Path | Format | Dims | License Status | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Smartphones Badge | `categories/cat_smartphones.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |
| Laptops Badge | `categories/cat_laptops.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |
| Audio Badge | `categories/cat_audio.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |
| Wearables Badge | `categories/cat_wearables.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |
| Tablets Badge | `categories/cat_tablets.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |
| Accessories Badge | `categories/cat_accessories.jpg` | JPEG | 1024 × 1024 | Authorized Luminex Asset | Horizontal Store Category Bar |

---

## 3. Brand & Campaign Motifs

| Asset Name | Relative Path | Format | ViewBox / Dims | License Status | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Festive Mandala Motif | `brand/mandala_accent.svg` | SVG | 600 × 600 | Proprietary (Original Luminex Asset) | Festive Store Header Artwork & Editorial Card Background |

---

## 3b. Editorial & Campaign Graphics

| Asset Name | Relative Path | Format | ViewBox / Dims | License Status | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Festive Music Banner | `editorial/festive_music.svg` | SVG | 400 × 400 | Proprietary (Original Luminex Asset) | Audio & Music promo card |
| Special Edition Engraved Buds | `editorial/special_buds_engraving.svg` | SVG | 400 × 360 | Proprietary (Original Luminex Asset) | Free Festive Engraving editorial card |
| Rangoli App on Device | `editorial/rangoli_app.svg` | SVG | 360 × 420 | Proprietary (Original Luminex Asset) | "Display your creativity" editorial card |
| Accessories Ensemble | `editorial/accessories_paired.svg` | SVG | 440 × 380 | Proprietary (Original Luminex Asset) | Accessories showcase card |
| Magenta Case Detail | `editorial/case_magenta.svg` | SVG | 320 × 400 | Proprietary (Original Luminex Asset) | Accessories case card with color swatches |
| Luminex Intelligence Glow | `editorial/luminex_intelligence.svg` | SVG | 500 × 360 | Proprietary (Original Luminex Asset) | AI & Aura Intelligence feature card |
| Continuity Ecosystem | `editorial/continuity.svg` | SVG | 520 × 360 | Proprietary (Original Luminex Asset) | Multi-device continuity feature card |
| Education Campus Bundle | `editorial/education_hero.svg` | SVG | 520 × 360 | Proprietary (Original Luminex Asset) | Education pricing savings card |
| Today at Luminex Workshop | `editorial/today_workshop.svg` | SVG | 440 × 340 | Proprietary (Original Luminex Asset) | Today at Luminex workshops card |
| Contactless Delivery Box | `editorial/delivery_box.svg` | SVG | 320 × 240 | Proprietary (Original Luminex Asset) | Free Delivery & Returns editorial card |

---

## 4. Central Product Image Mapping
Central mapping is defined in `store/management/commands/attach_assets.py` and stored in the Django database fields (`Product.main_image` and `Category.image`), allowing database-driven changes without altering HTML templates.
