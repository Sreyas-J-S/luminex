"""
Asset Generator for Luminex Storefront.
Creates original vector SVG assets matching Apple India Store aesthetic:
- Clean device renders (smartphones, laptops, earbuds, smartwatches, tablets, accessories)
- Category navigation icons
- Festive radiant mandala motif (Apple India festive campaign tribute)
"""
import os
import shutil

STATIC_PRODUCTS = "static/images/products"
STATIC_CATS = "static/images/categories"
STATIC_BRAND = "static/images/brand"
MEDIA_PRODUCTS = "media/products"
MEDIA_CATS = "media/categories"

# 1. Festive Mandala (Apple India Festive theme tribute)
MANDALA_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="mandalaGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff758c" stop-opacity="0.3"/>
      <stop offset="60%" stop-color="#ff7eb3" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="petalGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ec008c"/>
      <stop offset="50%" stop-color="#fc6767"/>
      <stop offset="100%" stop-color="#ffbe76"/>
    </linearGradient>
    <linearGradient id="petalGrad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff4b2b"/>
      <stop offset="100%" stop-color="#ff416c"/>
    </linearGradient>
    <linearGradient id="leafGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a8ff78"/>
      <stop offset="100%" stop-color="#78ffd6"/>
    </linearGradient>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <circle cx="300" cy="300" r="280" fill="url(#mandalaGlow)"/>

  <!-- Outer Petals Ring -->
  <g transform="translate(300, 300)">
    <!-- 12 Outer Petals -->
    <g id="petalRing">
      <path d="M 0,-240 C 35,-200 45,-150 0,-130 C -45,-150 -35,-200 0,-240 Z" fill="url(#petalGrad1)" opacity="0.85"/>
      <path d="M 0,-240 C 20,-205 25,-165 0,-140 C -25,-165 -20,-205 0,-240 Z" fill="#ffffff" opacity="0.35"/>
      <circle cx="0" cy="-250" r="5" fill="#fc6767"/>
    </g>
    <use href="#petalRing" transform="rotate(30)"/>
    <use href="#petalRing" transform="rotate(60)"/>
    <use href="#petalRing" transform="rotate(90)"/>
    <use href="#petalRing" transform="rotate(120)"/>
    <use href="#petalRing" transform="rotate(150)"/>
    <use href="#petalRing" transform="rotate(180)"/>
    <use href="#petalRing" transform="rotate(210)"/>
    <use href="#petalRing" transform="rotate(240)"/>
    <use href="#petalRing" transform="rotate(270)"/>
    <use href="#petalRing" transform="rotate(300)"/>
    <use href="#petalRing" transform="rotate(330)"/>

    <!-- Mid Petal Ring -->
    <g id="midPetal">
      <path d="M 0,-160 C 40,-130 35,-90 0,-70 C -35,-90 -40,-130 0,-160 Z" fill="url(#petalGrad2)" opacity="0.9"/>
      <circle cx="0" cy="-168" r="4" fill="#ec008c"/>
    </g>
    <use href="#midPetal" transform="rotate(15)"/>
    <use href="#midPetal" transform="rotate(45)"/>
    <use href="#midPetal" transform="rotate(75)"/>
    <use href="#midPetal" transform="rotate(105)"/>
    <use href="#midPetal" transform="rotate(135)"/>
    <use href="#midPetal" transform="rotate(165)"/>
    <use href="#midPetal" transform="rotate(195)"/>
    <use href="#midPetal" transform="rotate(225)"/>
    <use href="#midPetal" transform="rotate(255)"/>
    <use href="#midPetal" transform="rotate(285)"/>
    <use href="#midPetal" transform="rotate(315)"/>
    <use href="#midPetal" transform="rotate(345)"/>

    <!-- Inner Core Flower -->
    <circle cx="0" cy="0" r="60" fill="url(#petalGrad1)" filter="url(#softGlow)"/>
    <circle cx="0" cy="0" r="52" fill="#ffffff" opacity="0.85"/>
    <circle cx="0" cy="0" r="40" fill="url(#petalGrad2)"/>
    <circle cx="0" cy="0" r="22" fill="#ffffff"/>
    <circle cx="0" cy="0" r="14" fill="#fc6767"/>
  </g>
</svg>'''

# 2. Luminex Pro 15 (Flagship Smartphone with Titanium & Triple Lens)
PHONE_PRO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="proBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4a423f"/>
      <stop offset="50%" stop-color="#36302e"/>
      <stop offset="100%" stop-color="#1f1b1a"/>
    </linearGradient>
    <linearGradient id="titaniumRim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8c827a"/>
      <stop offset="50%" stop-color="#5a524c"/>
      <stop offset="100%" stop-color="#8c827a"/>
    </linearGradient>
    <radialGradient id="lensGlass" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#2a3b5c"/>
      <stop offset="40%" stop-color="#121824"/>
      <stop offset="100%" stop-color="#05080e"/>
    </radialGradient>
    <filter id="phoneShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <g filter="url(#phoneShadow)" transform="translate(130, 40)">
    <!-- Device Body -->
    <rect x="0" y="0" width="240" height="420" rx="42" fill="url(#titaniumRim)" stroke="#9c928a" stroke-width="2"/>
    <rect x="3" y="3" width="234" height="414" rx="40" fill="url(#proBody)"/>

    <!-- Camera Plateau -->
    <rect x="18" y="22" width="115" height="120" rx="28" fill="#2d2826" stroke="#4a423f" stroke-width="1.5"/>

    <!-- Lens 1 (Top Left) -->
    <circle cx="50" cy="54" r="22" fill="#1b1716" stroke="#5a524c" stroke-width="2.5"/>
    <circle cx="50" cy="54" r="16" fill="url(#lensGlass)"/>
    <circle cx="46" cy="50" r="4" fill="#ffffff" opacity="0.6"/>

    <!-- Lens 2 (Bottom Left) -->
    <circle cx="50" cy="110" r="22" fill="#1b1716" stroke="#5a524c" stroke-width="2.5"/>
    <circle cx="50" cy="110" r="16" fill="url(#lensGlass)"/>
    <circle cx="46" cy="106" r="4" fill="#ffffff" opacity="0.6"/>

    <!-- Lens 3 (Right Center) -->
    <circle cx="102" cy="82" r="22" fill="#1b1716" stroke="#5a524c" stroke-width="2.5"/>
    <circle cx="102" cy="82" r="16" fill="url(#lensGlass)"/>
    <circle cx="98" cy="78" r="4" fill="#ffffff" opacity="0.6"/>

    <!-- Flash & LiDAR -->
    <circle cx="102" cy="46" r="7" fill="#fffae6" stroke="#8c827a" stroke-width="1"/>
    <circle cx="102" cy="118" r="5" fill="#0d0f14"/>

    <!-- Brand Emblem -->
    <circle cx="120" cy="235" r="16" fill="none" stroke="#685f57" stroke-width="2.5"/>
    <circle cx="120" cy="235" r="6" fill="#8c827a"/>
  </g>
</svg>'''

# 3. Luminex Air 15 (Slim Vibrant Dual-camera Phone)
PHONE_AIR_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="airBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#dbe6ea"/>
      <stop offset="60%" stop-color="#b8ccd4"/>
      <stop offset="100%" stop-color="#9eb6c0"/>
    </linearGradient>
    <filter id="airShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000000" flood-opacity="0.18"/>
    </filter>
  </defs>

  <g filter="url(#airShadow)" transform="translate(135, 45)">
    <!-- Device Body -->
    <rect x="0" y="0" width="230" height="410" rx="38" fill="url(#airBody)" stroke="#ffffff" stroke-width="2"/>

    <!-- Camera Island (Vertical Dual Pill) -->
    <rect x="18" y="24" width="56" height="114" rx="28" fill="#cddde4" stroke="#e6f0f5" stroke-width="1.5"/>
    <circle cx="46" cy="52" r="19" fill="#1c2529" stroke="#9bb3bd" stroke-width="2"/>
    <circle cx="46" cy="52" r="13" fill="#0c1114"/>
    <circle cx="43" cy="49" r="3.5" fill="#ffffff" opacity="0.7"/>

    <circle cx="46" cy="110" r="19" fill="#1c2529" stroke="#9bb3bd" stroke-width="2"/>
    <circle cx="46" cy="110" r="13" fill="#0c1114"/>
    <circle cx="43" cy="107" r="3.5" fill="#ffffff" opacity="0.7"/>

    <!-- Flash -->
    <circle cx="95" cy="81" r="6" fill="#fffae6" stroke="#b0c4cc" stroke-width="1"/>

    <!-- Luminex Emblem -->
    <circle cx="115" cy="230" r="14" fill="none" stroke="#7e96a0" stroke-width="2"/>
    <circle cx="115" cy="230" r="5" fill="#7e96a0"/>
  </g>
</svg>'''

# 4. Luminex Book Pro 16 (Professional Laptop)
LAPTOP_PRO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="spaceBlack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2c2c2e"/>
      <stop offset="100%" stop-color="#161617"/>
    </linearGradient>
    <linearGradient id="displayScreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1c2438"/>
      <stop offset="40%" stop-color="#111929"/>
      <stop offset="70%" stop-color="#2d1b3e"/>
      <stop offset="100%" stop-color="#0a0a10"/>
    </linearGradient>
    <linearGradient id="screenArtwork" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0071e3"/>
      <stop offset="50%" stop-color="#ff2d55"/>
      <stop offset="100%" stop-color="#ff9f0a"/>
    </linearGradient>
    <filter id="laptopShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#000000" flood-opacity="0.22"/>
    </filter>
  </defs>

  <g filter="url(#laptopShadow)" transform="translate(45, 90)">
    <!-- Top Display Lid -->
    <rect x="40" y="0" width="330" height="215" rx="14" fill="url(#spaceBlack)" stroke="#48484a" stroke-width="1.5"/>
    <rect x="48" y="8" width="314" height="198" rx="8" fill="#000000"/>
    <!-- Screen Glass & Wallpaper Wave -->
    <rect x="50" y="10" width="310" height="194" rx="6" fill="url(#displayScreen)"/>
    <path d="M 50,150 Q 140,70 205,120 T 360,110 L 360,204 L 50,204 Z" fill="url(#screenArtwork)" opacity="0.65"/>
    <path d="M 50,170 Q 150,110 230,150 T 360,130 L 360,204 L 50,204 Z" fill="#0071e3" opacity="0.45"/>
    <!-- Camera Notch -->
    <rect x="195" y="8" width="20" height="7" rx="3" fill="#000000"/>
    <circle cx="205" cy="11" r="1.5" fill="#30d158"/>

    <!-- Bottom Chassis Base -->
    <polygon points="10,215 400,215 410,232 0,232" fill="#2c2c2e" stroke="#3a3a3c" stroke-width="1"/>
    <rect x="0" y="232" width="410" height="12" rx="4" fill="#1c1c1e"/>
    <!-- Display Hinge -->
    <rect x="155" y="214" width="100" height="3" fill="#0d0d0e"/>
    <!-- Opening Thumb Groove -->
    <rect x="180" y="232" width="50" height="3" rx="1.5" fill="#3a3a3c"/>
  </g>
</svg>'''

# 5. Luminex Buds Pro 3 (Earbuds & Case)
BUDS_PRO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="caseWhite" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#f2f2f4"/>
      <stop offset="100%" stop-color="#e1e1e4"/>
    </linearGradient>
    <filter id="caseShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.16"/>
    </filter>
  </defs>

  <g filter="url(#caseShadow)">
    <!-- Wireless Charging Case -->
    <rect x="135" y="150" width="230" height="180" rx="72" fill="url(#caseWhite)" stroke="#e5e5e7" stroke-width="1.5"/>
    <!-- Case Lid Seam -->
    <path d="M 137,215 L 363,215" stroke="#d2d2d7" stroke-width="1.5"/>
    <!-- Status LED -->
    <circle cx="250" cy="245" r="3.5" fill="#30d158"/>

    <!-- Left Earbud (Pop out) -->
    <g transform="translate(140, 75)">
      <circle cx="35" cy="30" r="24" fill="#ffffff" stroke="#e5e5e7" stroke-width="1"/>
      <rect x="30" y="42" width="14" height="42" rx="7" fill="#ffffff" stroke="#e5e5e7" stroke-width="1"/>
      <!-- Black vent grill -->
      <ellipse cx="38" cy="24" rx="8" ry="4" fill="#1d1d1f"/>
    </g>

    <!-- Right Earbud (Pop out) -->
    <g transform="translate(290, 75)">
      <circle cx="35" cy="30" r="24" fill="#ffffff" stroke="#e5e5e7" stroke-width="1"/>
      <rect x="26" y="42" width="14" height="42" rx="7" fill="#ffffff" stroke="#e5e5e7" stroke-width="1"/>
      <ellipse cx="32" cy="24" rx="8" ry="4" fill="#1d1d1f"/>
    </g>
  </g>
</svg>'''

# 6. Luminex Phones Max (Over-Ear Headphones)
HEADPHONES_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="silverMesh" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#d5d5d9"/>
      <stop offset="50%" stop-color="#efeff2"/>
      <stop offset="100%" stop-color="#d5d5d9"/>
    </linearGradient>
    <linearGradient id="aluminumCup" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#e8e8ed"/>
      <stop offset="100%" stop-color="#d0d0d5"/>
    </linearGradient>
    <filter id="hpShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.18"/>
    </filter>
  </defs>

  <g filter="url(#hpShadow)" transform="translate(75, 45)">
    <!-- Headband Arch (Steel Stem) -->
    <path d="M 75,230 C 75,70 275,70 275,230" fill="none" stroke="#b0b0b5" stroke-width="14" stroke-linecap="round"/>
    <!-- Canopy Knit Mesh -->
    <path d="M 95,200 C 95,95 255,95 255,200" fill="none" stroke="url(#silverMesh)" stroke-width="26" stroke-linecap="round"/>

    <!-- Left Ear Cup -->
    <g transform="translate(30, 200)">
      <rect x="0" y="0" width="75" height="110" rx="36" fill="url(#aluminumCup)" stroke="#d2d2d7" stroke-width="2"/>
      <rect x="4" y="8" width="20" height="94" rx="10" fill="#f0f0f3"/>
    </g>

    <!-- Right Ear Cup -->
    <g transform="translate(245, 200)">
      <rect x="0" y="0" width="75" height="110" rx="36" fill="url(#aluminumCup)" stroke="#d2d2d7" stroke-width="2"/>
      <rect x="51" y="8" width="20" height="94" rx="10" fill="#f0f0f3"/>
      <!-- Digital Crown dial -->
      <rect x="52" y="-5" width="15" height="8" rx="2" fill="#b0b0b5"/>
    </g>
  </g>
</svg>'''

# 7. Luminex Watch Ultra 2 (Rugged Smartwatch)
WATCH_ULTRA_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="tiCase" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5beb5"/>
      <stop offset="50%" stop-color="#9a9187"/>
      <stop offset="100%" stop-color="#7d756d"/>
    </linearGradient>
    <linearGradient id="oceanBand" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2a3036"/>
      <stop offset="50%" stop-color="#3c454e"/>
      <stop offset="100%" stop-color="#2a3036"/>
    </linearGradient>
    <filter id="watchShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000000" flood-opacity="0.22"/>
    </filter>
  </defs>

  <g filter="url(#watchShadow)" transform="translate(150, 45)">
    <!-- Top Strap -->
    <rect x="40" y="0" width="120" height="90" rx="12" fill="url(#oceanBand)"/>
    <!-- Bottom Strap -->
    <rect x="40" y="320" width="120" height="90" rx="12" fill="url(#oceanBand)"/>

    <!-- Rugged Titanium Case -->
    <rect x="10" y="70" width="180" height="270" rx="44" fill="url(#tiCase)" stroke="#d2c9bf" stroke-width="2"/>

    <!-- Orange Action Button -->
    <rect x="-3" y="150" width="6" height="50" rx="3" fill="#ff6b00"/>

    <!-- Crown & Side Button -->
    <rect x="187" y="130" width="9" height="55" rx="3" fill="#9a9187"/>
    <rect x="187" y="205" width="7" height="35" rx="2" fill="#7d756d"/>

    <!-- Screen Bezel & OLED Display -->
    <rect x="22" y="82" width="156" height="246" rx="34" fill="#000000" stroke="#1d1d1f" stroke-width="3"/>

    <!-- Wayfinder Watch Face -->
    <circle cx="100" cy="205" r="75" fill="none" stroke="#ff453a" stroke-width="2.5" stroke-dasharray="4 6"/>
    <text x="100" y="170" fill="#ffffff" font-family="-apple-system, sans-serif" font-size="28" font-weight="700" text-anchor="middle">09:41</text>
    <text x="100" y="210" fill="#ff9f0a" font-family="-apple-system, sans-serif" font-size="14" font-weight="600" text-anchor="middle">OCT 14 • 24°</text>
    <text x="100" y="240" fill="#30d158" font-family="-apple-system, sans-serif" font-size="13" font-weight="500" text-anchor="middle">COMPASS 315° NW</text>
  </g>
</svg>'''

# 8. Luminex Pad Pro 13 (Tablet)
PAD_PRO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="padBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38383a"/>
      <stop offset="100%" stop-color="#1c1c1e"/>
    </linearGradient>
    <linearGradient id="screenFluid" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00c6ff"/>
      <stop offset="50%" stop-color="#0072ff"/>
      <stop offset="100%" stop-color="#9b51e0"/>
    </linearGradient>
    <filter id="padShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.2"/>
    </filter>
  </defs>

  <g filter="url(#padShadow)" transform="translate(85, 45)">
    <!-- Chassis -->
    <rect x="0" y="0" width="330" height="410" rx="26" fill="url(#padBody)" stroke="#505054" stroke-width="1.5"/>
    <!-- Screen Glass -->
    <rect x="10" y="10" width="310" height="390" rx="18" fill="#000000"/>
    <rect x="14" y="14" width="302" height="382" rx="14" fill="url(#screenFluid)"/>

    <!-- Front Camera Dot -->
    <circle cx="165" cy="7" r="2" fill="#202022"/>

    <!-- Stylus Pencil docked on side -->
    <g transform="translate(322, 110)">
      <rect x="0" y="0" width="5" height="190" rx="2" fill="#ffffff" stroke="#e0e0e4" stroke-width="0.5"/>
      <polygon points="0,0 5,0 2.5,-10" fill="#dedee2"/>
    </g>
  </g>
</svg>'''

# 9. Luminex MagCharge 30W (Charger puck)
MAGCHARGE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="puckAlum" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#e8e8ed"/>
      <stop offset="100%" stop-color="#c8c8cd"/>
    </linearGradient>
    <filter id="magShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000000" flood-opacity="0.14"/>
    </filter>
  </defs>

  <g filter="url(#magShadow)" transform="translate(130, 110)">
    <!-- Woven Cable -->
    <path d="M 120,240 C 120,310 180,330 240,330" fill="none" stroke="#d5d5da" stroke-width="10" stroke-linecap="round"/>

    <!-- Puck Base Ring -->
    <circle cx="120" cy="120" r="115" fill="url(#puckAlum)" stroke="#dcdce0" stroke-width="2"/>
    <circle cx="120" cy="120" r="105" fill="#f8f8fa"/>
    <circle cx="120" cy="120" r="75" fill="none" stroke="#0071e3" stroke-width="4" stroke-dasharray="8 6"/>
    <circle cx="120" cy="120" r="30" fill="#0071e3" opacity="0.1"/>
    <!-- Lighting Bolt symbol -->
    <path d="M 122,95 L 110,122 L 122,122 L 118,145 L 134,118 L 122,118 Z" fill="#0071e3"/>
  </g>
</svg>'''

# 10. Luminex Smart Folio (Protective cover)
SMART_FOLIO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="folioDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2c3437"/>
      <stop offset="100%" stop-color="#192022"/>
    </linearGradient>
    <filter id="folioShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000000" flood-opacity="0.18"/>
    </filter>
  </defs>

  <g filter="url(#folioShadow)" transform="translate(100, 50)">
    <rect x="0" y="0" width="300" height="390" rx="16" fill="url(#folioDark)" stroke="#454f52" stroke-width="1.5"/>
    <!-- Fold Crease Lines -->
    <line x1="100" y1="0" x2="100" y2="390" stroke="#121718" stroke-width="3"/>
    <line x1="200" y1="0" x2="200" y2="390" stroke="#121718" stroke-width="3"/>
    <!-- Soft Touch Texture highlight -->
    <rect x="10" y="10" width="80" height="370" rx="8" fill="#ffffff" opacity="0.03"/>
    <!-- Camera square cutout -->
    <rect x="235" y="20" width="45" height="45" rx="10" fill="#151a1c"/>
  </g>
</svg>'''

# Category Icons (minimalist Apple store category icon row style)
CAT_ICONS = {
    'cat_smartphones.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <rect x="36" y="10" width="48" height="100" rx="12" fill="#1d1d1f" stroke="#86868b" stroke-width="2"/>
      <rect x="40" y="16" width="40" height="88" rx="8" fill="#43769b"/>
      <rect x="52" y="14" width="16" height="4" rx="2" fill="#000000"/>
    </svg>''',
    'cat_laptops.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <rect x="20" y="28" width="80" height="52" rx="4" fill="#1d1d1f" stroke="#86868b" stroke-width="1.5"/>
      <rect x="24" y="32" width="72" height="44" rx="2" fill="#0071e3" opacity="0.8"/>
      <polygon points="10,80 110,80 114,88 6,88" fill="#3a3a3c"/>
      <rect x="48" y="80" width="24" height="2" fill="#86868b"/>
    </svg>''',
    'cat_audio.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <rect x="32" y="42" width="56" height="46" rx="20" fill="#f5f5f7" stroke="#d2d2d7" stroke-width="2"/>
      <path d="M 33,60 L 87,60" stroke="#d2d2d7" stroke-width="1.5"/>
      <circle cx="50" cy="30" r="10" fill="#f5f5f7" stroke="#d2d2d7" stroke-width="1.5"/>
      <circle cx="70" cy="30" r="10" fill="#f5f5f7" stroke="#d2d2d7" stroke-width="1.5"/>
    </svg>''',
    'cat_wearables.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <rect x="45" y="8" width="30" height="24" rx="4" fill="#3a3a3c"/>
      <rect x="45" y="88" width="30" height="24" rx="4" fill="#3a3a3c"/>
      <rect x="34" y="26" width="52" height="68" rx="16" fill="#1d1d1f" stroke="#ff9f0a" stroke-width="2"/>
      <circle cx="60" cy="60" r="18" fill="none" stroke="#ff375f" stroke-width="2"/>
    </svg>''',
    'cat_tablets.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <rect x="25" y="12" width="70" height="96" rx="8" fill="#1d1d1f" stroke="#86868b" stroke-width="2"/>
      <rect x="28" y="16" width="64" height="88" rx="5" fill="#5856d6"/>
    </svg>''',
    'cat_accessories.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
      <circle cx="60" cy="60" r="38" fill="#f5f5f7" stroke="#86868b" stroke-width="2"/>
      <circle cx="60" cy="60" r="24" fill="none" stroke="#0071e3" stroke-width="3" stroke-dasharray="6 4"/>
      <circle cx="60" cy="60" r="8" fill="#0071e3"/>
    </svg>'''
}

PRODUCT_FILES = {
    'luminex_pro_15.svg': PHONE_PRO_SVG,
    'luminex_air_15.svg': PHONE_AIR_SVG,
    'luminex_mini_15.svg': PHONE_PRO_SVG,
    'luminex_book_pro_16.svg': LAPTOP_PRO_SVG,
    'luminex_book_air_15.svg': LAPTOP_PRO_SVG,
    'luminex_buds_pro_3.svg': BUDS_PRO_SVG,
    'luminex_phones_max.svg': HEADPHONES_SVG,
    'luminex_watch_ultra_2.svg': WATCH_ULTRA_SVG,
    'luminex_watch_series_9.svg': WATCH_ULTRA_SVG,
    'luminex_pad_pro_13.svg': PAD_PRO_SVG,
    'luminex_magcharge.svg': MAGCHARGE_SVG,
    'luminex_smart_folio.svg': SMART_FOLIO_SVG,
}

def main():
    print("Writing assets...")
    # Brand
    with open(os.path.join(STATIC_BRAND, "mandala_accent.svg"), "w") as f:
        f.write(MANDALA_SVG)
    with open(os.path.join("media/banners", "mandala_accent.svg"), "w") as f:
        f.write(MANDALA_SVG)

    # Products in static & media
    for filename, content in PRODUCT_FILES.items():
        with open(os.path.join(STATIC_PRODUCTS, filename), "w") as f:
            f.write(content)
        with open(os.path.join(MEDIA_PRODUCTS, filename), "w") as f:
            f.write(content)

    # Categories in static & media
    for filename, content in CAT_ICONS.items():
        with open(os.path.join(STATIC_CATS, filename), "w") as f:
            f.write(content)
        with open(os.path.join(MEDIA_CATS, filename), "w") as f:
            f.write(content)

    print("All vector assets written successfully.")

if __name__ == "__main__":
    main()
