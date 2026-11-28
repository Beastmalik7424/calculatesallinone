# AdSense readiness audit — 28 November 2026

- Production `ads.txt` returns HTTP 200 and the public AdSense ownership meta tag is present.
- `privacy`, `about`, `contact`, `terms`, `editorial-policy`, `methodology` and `affiliate-disclosure` pages return HTTP 200.
- Generated site has 42 indexable pages and 42 sitemap URLs. AdSense content-policy and monetization smoke tests pass.
- Production does not load `adsbygoogle.js`. The real `ADSENSE_SLOT` and `ADSENSE_CONSENT_READY` settings are absent. Ads remain disabled. A missing slot blocks ad activation, but is not by itself proof that site review is blocked because ownership meta and `ads.txt` are present.
- No CMP is currently active. Before personalized ads are served to EEA, UK or Switzerland visitors, use a Google-certified CMP integrated with IAB TCF. Verify that the CMP generates TCF v2.3 strings for strings created on or after 1 March 2026, as required by Google's publisher integration guidance. The privacy-policy wording in this branch now states the actual status instead of promising an undeployed consent flow.
- The private AdSense Sites page, Policy Center, account checks and review controls are not accessible through GitHub/Vercel. **No AdSense review was submitted.** Do not enable ads or mark consent ready until a real slot and required CMP are configured and tested.
- No fixed page-count or word-count threshold guarantees approval. Local content checks are evidence, not approval.
- No CSS/layout files were changed. Generated CSS from this build matches the live production asset byte-for-byte.

Official guidance: [AdSense page readiness](https://support.google.com/adsense/answer/7299563), [site ownership](https://support.google.com/adsense/answer/12131223), [program policies](https://support.google.com/adsense/answer/48182), [EEA/UK/Switzerland CMP requirements](https://support.google.com/adsense/answer/13554116), [Google publisher integration with IAB TCF](https://support.google.com/adsense/answer/9804260), which states that TCF v2.3 is mandatory for TC strings generated on or after 1 March 2026.

**Status: partially ready.** Ownership and content checks pass. Slot, consent implementation where required, and account-side review remain pending.
