# Beevoy — Premium Mānuka Honey Storefront (UI/UX Demo)

A responsive, interactive HTML/CSS/JavaScript storefront inspired by the Beevoy black-and-gold design direction, with a **Node.js server** and simple JSON API. Designed for **India (INR)** and **New Zealand (NZD)**.

## Run locally

1. Install **Node.js 18 or newer** from https://nodejs.org/ .
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Run:

   ```bash
   npm start
   ```

5. Visit **http://localhost:3000** in your browser.

No `npm install` is needed; this project uses only built-in Node.js modules. To run on another port (macOS/Linux): `PORT=4000 npm start`. For Windows PowerShell: `$env:PORT=4000; npm start`.

## Project files

```text
Beevoy_Fullstack/
├── package.json
├── server.js            # Node HTTP server and demo API
└── public/
    ├── index.html       # Homepage, listing, dialogs and shopping bag
    ├── styles.css       # Styling + responsive layouts
    └── app.js           # Product data loading, filters, markets and cart
```

## Interactive features

- Responsive homepage and mobile menu
- Filter sample products by collection
- Open product details and change quantity
- Add/remove cart products; persistent cart with localStorage
- Switch market between INR and NZD with corresponding *illustrative* pricing
- Review demo checkout totals through the server
- Newsletter demo form response through the server
- Keyboard Escape to dismiss overlays and basic accessible labels

## Node API

- `GET /api/health` — server status
- `GET /api/products` — sample product catalog
- `POST /api/newsletter` — validates email, **does not store it**
- `POST /api/checkout` — validates cart and calculates **demo** total, **does not place an order**

## Important before launch

This is a **visual and functional prototype**, not a production storefront. Product names, MGO grades, prices, packaging, country offerings, and all other marketing details are illustrative. Do **not** use them as verified product or health claims. Replace them with actual Beevoy data, confirm local regulations and certification rights, add production payment/shipping/tax/inventory/authentication integrations, and perform security and accessibility testing. Do not collect customer information with these endpoints until a proper privacy and data-handling system is implemented.

The stylized jars and scenery are created in CSS, so there are no missing stock photo files. Google Fonts are optional; local fallback fonts work offline.
