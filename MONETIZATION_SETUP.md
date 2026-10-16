# Monetization setup for CalculatesAll

## Current safe defaults

- AdSense is disabled unless both a real approved publisher ID and a real ad-unit slot ID are configured.
- The build does not invent an AdSense publisher ID.
- `ads.txt` is generated only when a valid `ADSENSE_CLIENT` is supplied.
- Marketplace links on `/marketplaces/` are official information/signup links, not affiliate links. No commission tracking is active by default.
- Never publish placeholder IDs or label an ordinary link as an affiliate link.

## Enable Google AdSense after approval

1. Open the Vercel project for this site.
2. Go to **Settings → Environment Variables**.
3. Add `ADSENSE_CLIENT` with the exact publisher ID Google gives you, such as the format `ca-pub-1234567890123456`.
4. Add `ADSENSE_SLOT` with the numeric ad-unit slot ID from the ad unit you created in AdSense.
5. Apply the variables to Production, then redeploy.

The values above are examples of the format only. Do not use them as real IDs. The build validates the publisher ID and numeric slot format. Ad serving still depends on Google approval, consent requirements, policy compliance, and Google being able to serve ads.

## Marketplace distribution

CalculatesAll is a website of browser-based tools. It does not automatically create listings or accounts on Etsy, Amazon, eBay, Gumroad or Daraz. Each platform requires a separate seller/affiliate account and policy review. If you decide to sell an original downloadable product, prepare the actual deliverable first (for example, a spreadsheet, printable worksheet or licensed source-code package), then upload it to the platform using your account.

Official starting points:
- Etsy digital downloads: https://www.etsy.com/ca/seller-handbook/article/47330319230
- Amazon Associates: https://affiliate-program.amazon.com/
- eBay Partner Network: https://partnernetwork.ebay.com/
- Gumroad: https://gumroad.com/features
- Daraz Pakistan seller portal: https://www.daraz.pk/sell/

Affiliate programmes have separate eligibility, country, payout, tracking and disclosure requirements. Add only real approved tracking links or IDs. Do not copy product images, brand assets or listings without permission.
