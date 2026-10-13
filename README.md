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
- 🛡️ **Security & Robustness** — CSRF protection, transactional checkout, stock race-condition safety, and 24 passing automated tests
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
git clone https://github.com/yourusername/luminex.git
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

```
SECRET_KEY=<generate a strong secret key>
DEBUG=False
ALLOWED_HOSTS=yourapp.onrender.com
DATABASE_URL=<your PostgreSQL internal URL from step 1>
DJANGO_SETTINGS_MODULE=luminex.settings.production
```

### 4. Deploy

Push to your GitHub repository connected to Render, or trigger a manual deploy.

### 5. Create admin user on Render

After deployment, run a one-off command in the Render Shell:
```bash
python manage.py createsuperuser
# Or seed demo data:
python manage.py seed_demo
```

### Media Files (Production)

For production, uploaded media files (product images, banner images) require object storage. Options:
- **AWS S3** — Install `django-storages` and `boto3` (already in requirements.txt) and set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`
- **Cloudinary** — Alternative cloud image storage
- **Render Disk** — Attach a persistent disk to your web service (simple but limited)

> ⚠️ Render's ephemeral filesystem means uploaded files are **lost on redeploy** unless you use S3 or a Render Disk.

---

## 🎨 Design System

The CSS design system uses CSS custom properties (variables) for complete consistency:

```css
:root {
  --color-charcoal: #1d1d1f;   /* Primary dark */
  --color-blue: #0071e3;        /* Action blue */
  --color-off-white: #f5f5f7;   /* Background */
  --font-family: 'Inter', system-ui, sans-serif;
}
```

Key components: `.navbar`, `.hero-slider`, `.product-card`, `.category-card`, `.promo-card`, `.btn`, `.auth-card`, `.profile-grid`

---

## 📝 Incomplete Features / Future Work

The following are **not implemented** in this version and require additional work:

1. **Shopping Cart / Checkout** — UI stub exists ("Add to Cart" button) but no cart model or checkout flow
2. **Order Management** — No Order model or order history
3. **Payment Integration** — Razorpay/Stripe not integrated
4. **Media file cloud storage** — Requires S3 or Cloudinary setup for production
5. **Email verification** — Registration doesn't send a verification email
6. **Wishlist** — Not implemented
7. **Product reviews/ratings** — Not implemented
8. **Pagination** — Product list uses all results (add `django.core.paginator` for large catalogues)

---

## 📄 License

MIT License — free to use and modify for personal and commercial projects.

---

*Built with ❤️ using Django 5.0 • Luminex Technologies Pvt. Ltd.*
