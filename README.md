# Final Vending Machine (Tkinter)

Interactive drink vending machine GUI written in Python with Tkinter. It supports multiple drink categories, temperature styles, loyalty points, coupons, and an admin dashboard with revenue reporting.

## Quick start
- Requirements: Python 3.9+ (Tkinter included on Windows).  
- Run: `python "Vending machine (FINAL TEST).py"`
- Assets: drink images live in `Drinks/`, logo in `LOGO.png` (bundled).

## Features
- 20 illustrated drinks grouped by category (coffee, tea, milk, sodas, protein shakes, recommendations, others).
- Hot / Cold / Blended style selector that updates every button label in real time.
- Balance handling with input validation and change display.
- Loyalty program: points per purchase, automatic coupon generation at 4 points, 50% off coupon application.
- Phone-based customer lookup so points/coupons follow the customer.
- Admin dashboard showing total sales count, revenue, and scrollable purchase history.

## Using the app
1) Pick a category, then click a drink card (image + name).  
2) Choose style (`Hot`, `Cold`, `Blended`) if desired.  
3) Enter money and click **Insert**.  
4) Click **Purchase**; you’ll be asked for a phone number to earn points and coupons.  
5) Redeem coupons via **Use Coupon (50% off)** before purchasing.  
6) Admins: click **Admin** (top-right) to see live sales and revenue stats.

## File map
- `Vending machine (FINAL TEST).py` – main Tkinter app.
- `Drinks/` – PNG assets for each drink button.
- `LOGO.png` – top banner logo.
- `คู่มือการใช้งาน.txt` – Thai user guide.

## Notes
- Points needed for a coupon: `points_needed_for_coupon = 4` (change in code if you want a different threshold).
- Prices are set per drink inside `self.drinks`; adjust there for menu or currency changes.
- Balance, revenue, and histories are in-memory; persistence would require a small data layer (e.g., SQLite or JSON saves) if you need it across runs.
