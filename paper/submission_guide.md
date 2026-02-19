# Submission and Publication Guide (Updated: February 19, 2026)

## 1) Literature Gap Check (Was this already done by others?)

### Search focus
I checked whether a peer-reviewed paper already exists that combines all of the following in CFPS reactor-format selection:
1. PRISMA-style literature extraction
2. cross-format yield/time normalization
3. scenario-weighted MCDA decision matrix

### What was found
Closest papers were method reviews and domain reviews, not a full PRISMA + scenario-MCDA decision framework:
1. Gregorio et al., *A User's Guide to Cell-Free Protein Synthesis* (Methods Protoc, 2019): practical workflow guidance, no scenario-weighted MCDA.
   - https://doi.org/10.3390/mps2020024
2. Damiati et al., *Cell-Free Approaches in Synthetic Biology Utilizing Microfluidics* (Genes, 2018): microfluidics-focused review, no cross-format MCDA.
   - https://doi.org/10.3390/genes9030144
3. Silverman et al., *Cell-free gene expression: an expanded repertoire of applications* (Nat Rev Genet, 2020): broad review, no reactor-format decision matrix.
   - https://doi.org/10.1038/s41576-019-0186-3
4. PubMed targeted query for CFPS + MCDA (run on 2026-02-19) returned no direct match.
   - https://pubmed.ncbi.nlm.nih.gov/?term=%28%22cell-free+protein+synthesis%22+OR+CFPS%29+AND+%28%22multi-criteria+decision+analysis%22+OR+MCDA+OR+%22decision+matrix%22%29

### Practical conclusion
Based on this targeted check, your current work appears novel in its exact combination of PRISMA-informed extraction and scenario-weighted MCDA for CFPS reactor formats.

## 2) Where to Submit (Best-fit journal options)

## Option A: Synthetic Biology (Oxford University Press)
Why fit:
1. Focus on synthetic biology methods, platforms, and design frameworks.
2. Your work is a quantitative decision framework with clear synthetic-biology utility.

Submission info:
1. Author instructions: https://academic.oup.com/synbio/pages/instructions_to_authors
2. Online submission system (ScholarOne) is listed on that page.

## Option B: ACS Synthetic Biology
Why fit:
1. High relevance to CFPS platform and method-development work.
2. Good visibility for synthetic-biology tool papers.

Submission info:
1. ACS author preparation: https://researcher-resources.acs.org/publish/preparing-your-manuscript
2. Submission via ACS Publishing Center (linked from ACS author resources).

## Option C: Frontiers in Bioengineering and Biotechnology
Why fit:
1. Accepts applied platform papers and methodology work in bioengineering/synthetic biology.
2. Usually straightforward editorial workflow for methods papers.

Submission info:
1. Author guidelines: https://www.frontiersin.org/journals/bioengineering-and-biotechnology/for-authors/author-guidelines
2. Frontiers online submission platform is used.

## Option D: Biochemical Engineering Journal (Elsevier)
Why fit:
1. Reactor/process comparison and decision frameworks fit biochemical-engineering scope.
2. Strong process-oriented audience.

Submission info:
1. Guide for authors: https://www.sciencedirect.com/journal/biochemical-engineering-journal/publish/guide-for-authors
2. Online submission link is provided on the guide page.

## Option E: PLOS ONE
Why fit:
1. Methodologically sound cross-disciplinary studies are in scope.
2. Good fallback if novelty is moderate but reproducibility is strong.

Submission info:
1. Submission guidelines: https://journals.plos.org/plosone/s/submission-guidelines

## 3) Recommended Submission Path (for this manuscript)
1. Primary target: `Synthetic Biology` or `ACS Synthetic Biology`.
2. If desk-rejected for scope, transfer to `Frontiers in Bioengineering and Biotechnology`.
3. If needed, use `PLOS ONE` as robustness-focused fallback.

## 4) Step-by-step submission checklist
1. Select one target journal and adapt manuscript structure to that journal template.
2. Convert figures to required resolution and format (you already have PNG/TIFF outputs under `figures/`).
3. Prepare supplementary package:
   - cleaned dataset
   - MCDA tables
   - PRISMA flow figure
   - protocol files
4. Write a sharp cover letter with:
   - research gap
   - novelty claim (no prior PRISMA + scenario-MCDA CFPS framework found)
   - practical impact for reactor selection
5. Verify every DOI in the references before upload.
6. Add author metadata in submission system (affiliation, funding, competing interests, CRediT).
7. Suggest 3-5 potential reviewers from recent CFPS/CFSE and microfluidic CFPS literature.
8. Submit, then address reviewer comments with a point-by-point response table.

## 5) Google Scholar profile and indexing (important)

### Do you need a Google Scholar account to publish?
No. Journal submission and publication do not require a Google Scholar profile.

### Should you still create one?
Yes. It helps citation tracking, visibility, and quick sharing of your publication list.

### How to create your profile
1. Go to Google Scholar profile page: https://scholar.google.com/intl/en-US/scholar/citations.html
2. Sign in with a Google account.
3. Add name, affiliation, institutional email (recommended), and research interests.
4. Choose automatic or manual article updates.

### Can you manually "upload a paper" to Google Scholar?
Not directly as a publisher upload. Scholar indexes content automatically from publisher sites and repositories.
Source: Google Scholar inclusion guidance for webmasters states automated indexing and no manual requests.
- https://scholar.google.com/intl/en/scholar/inclusion.html

## 6) Immediate next actions for your case
1. Decide first target journal (`Synthetic Biology` or `ACS Synthetic Biology`).
2. Match manuscript formatting to that journal.
3. Prepare cover letter and supplementary files.
4. Submit and archive the submitted version in your repo with date tag.
