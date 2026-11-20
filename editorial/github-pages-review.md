# GitHub Pages setup for the author review edition

The review branch is `review/author-review-2026-11-20`. Its workflow builds the
clean HTML book and the matching whole-book PDF. It publishes only `_book/`.
Word review files, comments, tracked changes and private editorial records are
excluded from Git and the site.

Publishing is initially disabled. A push builds and checks a downloadable
Actions artifact. The repository variable `PUBLISH_REVIEW` must be set to the
exact value `true` before a build can deploy. The prominent draft banner remains
on every HTML page, and the PDF has a draft page header. This is the review
edition; author approval and final publication metadata remain pending.

## Set up the repository

1. Open the repository's **Settings → Actions → General** and allow GitHub
   Actions, including the `actions/*` and `quarto-dev/quarto-actions/*` actions
   used by this repository. The workflow declares its own required token
   permissions; broad repository write permission is unnecessary.
2. In **Settings → Pages**, set **Build and deployment → Source** to
   **GitHub Actions**. Do not select a source-code folder for branch publishing.
3. In **Settings → Environments**, open or create `github-pages`. Under its
   deployment branch rules, allow `review/author-review-2026-11-20`. If the
   environment initially allows only the default branch, change that rule to
   permit the review branch. Required reviewers can be added if desired.
4. In **Settings → Secrets and variables → Actions → Variables**, create the
   repository variable `PUBLISH_REVIEW` with the value `true` when ready to make
   the draft publicly accessible. No additional publishing secret is needed.
5. Trigger a fresh push to the review branch after completing these settings.
   The following commands work even when this workflow is not on the default
   branch:

   ```powershell
   git switch review/author-review-2026-11-20
   git commit --allow-empty -m "Enable the public author review draft"
   git push origin review/author-review-2026-11-20
   ```

6. Open **Actions → Build and publish review draft** and wait for both `build`
   and `deploy` to complete. Use the URL reported by the deployment job or by
   **Settings → Pages**. Check the home page, a chapter on a phone-width display,
   and the PDF download before sharing that URL with authors.

The expected project-site address, if this repository is served under the
account's ordinary GitHub Pages domain, is
`https://jamessteeleii.github.io/sport-exercise-research-methods-primer/`.
This is a setup expectation, not a claim that a deployment has been verified.
The metadata ledger leaves `site_url` unset until the actual deployed address
has been confirmed. No custom domain is configured.

The **Run workflow** button requires the workflow to exist on the default
branch. A push to the dedicated review branch is therefore the reliable first
trigger. There is no need to merge the book into `main` to use the push trigger.

## Later review updates

Transfer agreed author changes deliberately into the Quarto files, rebuild and
check the proofs, then commit and push to the same review branch. With
`PUBLISH_REVIEW=true`, subsequent pushes update the public draft automatically.
Keep the exact Word files sent and returned privately, and retain each review
package manifest so that changes can be compared against the right version.

To stop automatic deployments, set `PUBLISH_REVIEW` to `false` or delete the
variable. This does not remove an already deployed site; use the GitHub Pages
settings if the existing public draft needs to be unpublished.

## Official documentation

- [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Configuring the publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
