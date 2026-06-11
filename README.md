# PhD Shortlist Builder

An automated discovery and evaluation system that produces personalized, evidence-backed PhD shortlists for students based on regional grant and job APIs.

## How to Run

### Prerequisites
- **Conda**: Ensure you have Conda installed.
- **Environment**: The project uses the `phd-builder` environment.
- **API Keys**: Configure your `.env` file with `HF_TOKEN` (Hugging Face).

### Setup
```bash
# Create the environment from the provided file
conda env create -f environment.yml
conda activate phd-builder
```

### Execution
1. Add student profiles to `input.json`.
2. Run the main pipeline:
```bash
conda run -n phd-builder python main.py
```
3. Results will be saved as `output_YYYY-MM-DD_HH-MM-SS.json`.

## Data Sources
The system uses a modular provider architecture:
- **OpenAlex API**: Global discovery via publication and grant-funder metadata (UK, CA, AU fallback).
- **NIH RePORTER**: Direct access to active U.S. research grants and PIs.
- **Euraxess RSS**: Live PhD vacancies and job postings across Europe.

## Approach Overview
Our approach focuses on **High-Confidence Discovery**. Instead of broad keyword searches, we target **active research grants**. An active grant is a strong indicator of both funding and an open research direction. We then use a phased LLM evaluation (Llama-3.1-8B) to score candidates on Position, Focus, and Technical Evidence.

## Design Trade-offs
- **Strict Filtering**: We enforce a Score >= 50 threshold. This ensures quality but requires a large initial fetch (300+ candidates) to meet the 50-200 recommendation goal.
- **Verifiable Links**: Every recommendation must have a DOI or Grant URL. Candidates without traceable links are filtered out early in the pipeline.

## Known Limitations
- **Email Access**: Public APIs often mask PI emails for privacy; these are marked "N/A" unless found in metadata.
- **Citizenship Filters**: While we filter by country, specific "Home Fees only" restrictions in free-text ads are not yet fully parsed and require manual student check.
