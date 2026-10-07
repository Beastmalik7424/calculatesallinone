# Upload guide (follow in order)

## What is in this folder
Everything in this folder goes to GitHub. Do not upload the folder itself, upload its contents.

## Part 1: GitHub
1. Open github.com and log in.
2. If you already have the repository, open it. If not, click the + at the top right, then "New repository", name it calculateallinone, keep it Public, and click "Create repository".
3. In your repository, click "Add file", then "Upload files".
4. Open this folder on your computer, select all the files and folders inside it (Ctrl+A or Cmd+A), and drag them into the upload box.
5. If old files are in the repository (for example an old index.html in the main folder), delete them first: click the file, the bin icon, then "Commit changes".
6. Scroll down, type "CalculatesAll v8" in the box, and click "Commit changes".

Note: some computers do not upload hidden folders like ".github". The site still works without it. The .github folder only runs automatic checks.

## Part 2: Vercel
1. Open vercel.com and click "Log in" with GitHub.
2. If your project already exists: open it, go to Settings, then Git, and check that it shows your repository. Then go to Settings, then Build and Deployment, and set:
   - Framework Preset: Other
   - Build Command: npm run build
   - Output Directory: public
3. If the project does not exist: click "Add New", then "Project", then "Import" next to your repository. Set the same three values above.
4. Still in Settings, open "Environment Variables" and add:
   - Name: CONTACT_EMAIL   Value: malikadeelbhatti@gmail.com
   - Name: SITE_URL   Value: https://calculateallinone.vercel.app   (use your real address)
5. Click "Deploy" (or "Redeploy" on the Deployments tab). Wait until the status says Ready.

## Part 3: Check the live site
1. Open your site address. You should see the homepage with the category list.
2. Open /zakat-calculator/ and /ur/ to check the pages load.
3. Open /sitemap.xml and /robots.txt. You should see text, not an error.

## Part 4: Google Search Console (after the site is live)
1. Open search.google.com/search-console and add your site.
2. Choose Sitemaps in the left menu, type sitemap.xml, and click Submit.

## Later, when you have these
- AdSense ID: add a variable named ADSENSE_CLIENT in Vercel, then redeploy.
- Reviewer details for Zakat and BMI: send them to me.
- Native-reader corrections: send the file review/translations_review.csv back to me.
