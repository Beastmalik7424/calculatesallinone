# CalculatesAll

Static calculator site. Vercel runs npm run build on every push to main. The build compiles Tailwind CSS and then generates every page, the sitemap, robots.txt, the favicon and the Open Graph image.

## What is in the repository

- build.py holds the tool content, guides, FAQs, Urdu pages, hub pages and the page templates. Edit content here.
- static/app.js holds all calculator logic. It uses no eval and no Function constructor. Zakat and BMI messages are available in English and Urdu.
- styles/input.css and tailwind.config.js control the compiled stylesheet. Tailwind scans build.py and static/app.js, so class names must appear literally in those files.
- static/ads.txt is the ads.txt file. Replace the placeholder line after AdSense approval.
- vercel.json sets the build command, output folder, clean URLs and security headers.
- .github/workflows/checks.yml runs the same build on every pull request and checks titles, canonicals, descriptions, assets and JSON-LD.

## URL structure

- / and /ur/ are the English and Urdu home pages.
- /money/, /health/, /time/, /math/ and /worship/ are category hub pages.
- Each tool has its own URL, for example /zakat-calculator/. Zakat and BMI also have Urdu pages under /ur/.
- /about/, /privacy/, /contact/ and /404 are supporting pages.
- hreflang links join each English page to its Urdu counterpart. The sitemap includes the same pairs.

## One-time setup

1. Create an empty repository on GitHub, for example calculateallinone.
2. From this folder, run:

```
git init
git add .
git commit -m "CalculatesAll site v2"
git branch -M main
git remote add origin https://github.com/YOUR-USER/calculateallinone.git
git push -u origin main
```

3. In Vercel, choose Add New, then Project, then import the GitHub repository.
4. Keep the framework preset as Other. The build command and output folder come from vercel.json.
5. In Project Settings, then Environment Variables, add these values:
   - SITE_URL with your live address, for example https://calculateallinone.vercel.app
   - CONTACT_EMAIL with the address shown on the contact page
   - ADSENSE_CLIENT with your ca-pub number, only after AdSense approval

## Automatic updates

- Every push to main deploys to production.
- Every pull request gets a preview URL from Vercel and runs the checks workflow on GitHub.
- To change content, edit build.py or static/app.js, commit, and push.

## Before going live

- If you enable advertising, configure the Google certified consent message in AdSense for EEA and UK visitors. The privacy page describes this.
- Replace the placeholder publisher line in static/ads.txt with the line from your AdSense account.
- Have a qualified scholar review the Zakat wording and a health professional review the BMI wording. The Urdu text was written for this release and should also be checked by a native reader.
- Submit sitemap.xml in Google Search Console after the production deploy, and confirm both the English and Urdu URLs are indexed.

## Reviewers (Zakat, BMI and any future guide)

Create reviewers.json in the repository root only when you have a real, consenting reviewer. The file is optional. Without it, pages show "review pending".

```
{
  "zakat-calculator": {
    "name": "Full name of the qualified reviewer",
    "credentials": "Their qualification, for example Mufti or Doctor, with the body that certifies it",
    "bio": "Two sentences on their relevant experience",
    "review_date": "YYYY-MM-DD of the review",
    "scope": "What exactly they reviewed"
  }
}
```

The build then shows a reviewer box on that page and adds Person schema. Never add a reviewer you have not confirmed with.

## AdSense

Set ADSENSE_CLIENT to your ca-pub number. The build writes ads.txt with the matching publisher line and adds the ad script. Without it, ads.txt keeps a placeholder and no ad code is added.

## Translation review

The build writes review/translations_review.csv with every Arabic, Hindi, Spanish, French and Urdu string. Send this file to native readers. They fill reviewer_status, reviewer_correction and reviewer_name. Apply corrections in lang_v6.py or urdu_v5.py and rebuild.

## Performance audit after deploy

Run bash scripts/lighthouse-audit.sh https://your-domain on a machine with Chrome. Reports are saved in lighthouse-reports/.
