# Luminex Store

**Premium Electronics E-Commerce Platform — Illuminate Your World**

A complete, production-ready Django e-commerce website built with a premium minimalist design inspired by high-end electronics storefronts. Features full product management, dynamic banner management, user authentication, and a rich admin dashboard.

---

## ✨ Features

- 🏠 **Apple India Store Experience** — Gradient "Store." greeting header, festive Indian mandala backdrop motif, concierge specialist links, and No Cost EMI announcement ribbon
- 🏷️ **Horizontal Category Navigation** — Apple-style device strip for Smartphones, Laptops, Audio, Wearables, Tablets, and Accessories
- 🎠 **Horizontal Product Carousels** — "The latest" new arrivals with glass circular controls, touch/mouse smooth scroll snap, and Dark Titanium theme cards
- 🌟 **Editorial Collections** — "The Luminex Difference" cards featuring No Cost EMI offers, device Trade In, free delivery, and personalized setup
- 🛍️ **Interactive Shopping Bag** — Persistent session/user cart, live item count badge in navbar, quantity steppers, item removal, and free delivery threshold tracker
- 💳 **Streamlined Checkout & Order Management** — Multi-step checkout with server-side price validation, atomic inventory deduction, unique order numbers (`LMX-...`), order confirmation receipts, and profile order history
- 📦 **Product Detail Pages** — Multi-image gallery, real "Add to Bag", stock status indicators, warranty and delivery perks, and related products
- 🎯 **Dynamic Banner Management** — Create, edit, delete, enable/disable hero and promotional banners with image uploads
- 👤 **Authentication & Profile** — User registration, login, logout, profile update, and order history tracking
- 🛡️ **Security & Robustness** — CSRF protection, transactional atomic checkout, PostgreSQL deadlock prevention, cryptographic idempotency nonces, order authorization permissions, and 55 passing automated tests
- 🚀 **Production Ready** — WhiteNoise static files, Gunicorn, PostgreSQL support, and Render build configuration


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13 + Django 5.0 |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL |
| Frontend | HTML5, CSS3, Vanilla JS |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Deployment | Render |
| Image Handling | Pillow |

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Sreyas-J-S/luminex.git
cd luminex
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings (SECRET_KEY required)
```

Generate a secret key:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Seed demo data (creates admin user + sample products)

```bash
python manage.py seed_demo
```

**Default admin credentials:** `admin` / `admin123`

### 7. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ | insecure dev key | Django secret key |
| `DEBUG` | | `True` | Debug mode |
| `ALLOWED_HOSTS` | | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DATABASE_URL` | Prod only | — | PostgreSQL connection URL |
| `EMAIL_HOST` | | `smtp.gmail.com` | SMTP host |
| `EMAIL_PORT` | | `587` | SMTP port |
| `EMAIL_HOST_USER` | | — | SMTP username |
| `EMAIL_HOST_PASSWORD` | | — | SMTP password |

---

## 📁 Project Structure

```
luminex/
├── manage.py
├── requirements.txt
├── Procfile                    # Gunicorn process
├── build.sh                    # Render build script
├── .env.example                # Environment variable template
├── .gitignore
│
├── luminex/                    # Django project config
│   ├── settings/
│   │   ├── base.py             # Shared settings
│   │   ├── local.py            # SQLite, debug=True
│   │   └── production.py       # PostgreSQL, security headers
│   ├── urls.py                 # Root URL config
│   └── wsgi.py
│
├── store/                      # Main e-commerce app
│   ├── models.py               # Category, Product, ProductImage, Banner
│   ├── views.py                # home, product_list, product_detail, category_detail
│   ├── urls.py
│   ├── admin.py                # Rich admin with image previews
│   ├── context_processors.py  # nav_categories available globally
│   └── management/commands/
│       └── seed_demo.py        # Demo data seeder
│
├── accounts/                   # Auth app
│   ├── views.py                # register, login, logout, profile
│   ├── urls.py
│   └── forms.py                # RegisterForm, LoginForm, ProfileUpdateForm
│
├── templates/
│   ├── base.html               # Base with navbar, footer, messages
│   ├── store/
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── category_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   └── partials/
│   │       └── product_card.html
│   └── accounts/
│       ├── register.html
│       ├── login.html
│       └── profile.html
│
├── static/
│   ├── css/style.css           # Complete design system
│   └── js/main.js              # Slider, mobile nav, gallery, animations
│
└── media/                      # Uploaded images (git-ignored)
```

---

## 🧪 Running Tests

```bash
# Built-in Django test runner
python manage.py test

# Test specific app
python manage.py test store
python manage.py test accounts
```

### Manual Test Checklist

- [ ] Homepage loads with hero banner and categories
- [ ] Products page shows all 11 demo products
- [ ] Search returns relevant results
- [ ] Category filter works
- [ ] Sort (price, name, date) works
- [ ] Product detail page loads with price and stock
- [ ] User registration works
- [ ] Login with registered user works
- [ ] Profile page is accessible after login
- [ ] Profile update saves changes
- [ ] Logout redirects to homepage
- [ ] Accessing `/accounts/profile/` while logged out redirects to login
- [ ] Admin `/admin/` accessible with admin/admin123
- [ ] Admin can add/edit/delete products, categories, banners

---

## 🌐 Admin Dashboard

URL: `http://127.0.0.1:8000/admin/`

**Default credentials:** `admin` / `admin123`

### What you can manage:

| Model | Features |
|-------|----------|
| **Products** | Name, description, price, original price (for discounts), images, category, stock, active/featured/new arrival flags |
| **Categories** | Name, slug, description, image, active status, sort order |
| **Banners** | Title, subtitle, description, CTA button, image, background colour, text colour, position (hero/promo), active status |
| **Users** | All Django built-in user management |

---

## 🚀 Deployment on Render

### 1. Create a PostgreSQL database on Render

In your Render dashboard, create a new PostgreSQL database and copy the **Internal Database URL**.

### 2. Create a Web Service on Render

- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn luminex.wsgi --log-file -`
- **Python version:** 3.13

### 3. Set Environment Variables on Render

In your Web Service settings → Environment:

```env
SECRET_KEY=<generate a strong secret key>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-app-name>.onrender.com
DATABASE_URL=<your PostgreSQL Internal Database URL from Render>
DJANGO_SETTINGS_MODULE=luminex.settings.production

# Persistent Media Storage (AWS S3 or Cloudflare R2):
AWS_STORAGE_BUCKET_NAME=<your-s3-or-r2-bucket-name>
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_S3_REGION_NAME=us-east-1
# AWS_S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com  # (Only if using Cloudflare R2)
```

### 4. Deploy

Connect your GitHub repository to Render and trigger a manual or automatic deploy. The `build.sh` script automatically installs dependencies, collects static assets via WhiteNoise, and applies database migrations.

### 5. Create admin user & seed demo data on Render

After initial deployment, open the **Shell** tab on Render and run:
```bash
python manage.py seed_demo
```
This provisions default categories, banners, and sample products.

### Media Files (Production)

Render's Web Services run on an ephemeral container filesystem. Any file written to the local disk is destroyed whenever the service restarts or redeploys. To ensure product images and promotional banners persist indefinitely:
- **AWS S3 / Cloudflare R2 / Backblaze B2:** Already integrated using `django-storages[boto3]`. Simply supply `AWS_STORAGE_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` in Render environment variables.
- When those environment variables are omitted (e.g. local development or test suites), Luminex automatically falls back to standard local file storage without requiring any cloud credentials.

---

## 🎨 Design System & Accessibility

The CSS design system follows Apple HIG principles:
- **Design Tokens:** Modern CSS variables for colors, typography, elevations, and transitions.
- **Accessibility:**
  - Skip-to-main-content keyboard link (`.skip-link`)
  - WCAG 2.1 AA compliant text contrast (`--color-silver: #6e6e73` with 5.44:1 contrast ratio)
  - Clear `:focus-visible` keyboard rings
  - Full support for `prefers-reduced-motion: reduce` across sliders, carousels, and animations.
- **Checkout Reliability:** Double-click submit disabling with spinner state, server-side idempotency tokens, and row-level stock locks.

---

## 📝 Roadmap & Optional Extensions

The following are optional future enhancements:
1. **Third-party Payment Gateway** — Razorpay / Stripe webhook integration (currently supports card/UPI simulated payment flow)
2. **Transactional Email Service** — Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` to hook into SendGrid or Amazon SES
3. **Product Reviews & Ratings** — User star ratings and text feedback on product detail pages
4. **Wishlist** — Saved products list for registered users

---

## 📄 License

MIT License — free to use and modify for personal and commercial projects.

---

*Built with ❤️ using Django 5.0 • Luminex Technologies Pvt. Ltd.*
