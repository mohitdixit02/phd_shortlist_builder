# How we built the PhD Shortlist system

This document explains the "why" behind our technical choices. It’s a look under the hood at how we make sure every student gets a shortlist that actually makes sense for their future.

## 1. Cleaning up the noise (The Builder Phase)
AI gets confused by huge walls of text. If we just hand it a 10-page CV and a bunch of research papers, it loses focus. 
- **The Fix**: We take all that raw info—resumes, notes, and old papers—and boil it down into a sharp, 2-3 line "Intent" blurb.
- **Why it matters**: By focusing on the student's *actual goal* rather than just their history, the AI makes much smarter decisions.

## 2. Setting the ground rules (Strict Filtering)
We don't want to waste time (or AI tokens) on supervisors who aren't a basic match. Before the AI even looks at a candidate, we apply two deal-breaker rules:
- **Location**: If a student wants the UK, we instantly drop anyone outside the UK. 
- **Proof of Work**: Every supervisor *must* have a working link to a recent paper or grant. No link, no entry. We only recommend people whose work is verifiable.

## 3. Our Two-Pass Check
Checking everything at once is messy and slow. Instead, we use a two-step "filter" approach:
- **Pass 1: The Essentials**: We check **Position** (is there an opening?) and **Focus** (is the research area right?). If a supervisor scores below 50 on either, they are rejected immediately. This keeps our shortlist high-quality.
- **Pass 2: The Technical Deep-Dive**: Only if they pass the first step do we check **Evidence**. We look at the supervisor’s actual technical track record to see if it matches the student’s specific skills (like coding or lab techniques). **If this technical fit is low (under 50), they’re out.**

## 4. The three questions students actually ask
We chose **Position, Focus, and Evidence** because they answer the three biggest questions a student has:
1. **Is there a job?** (Position)
2. **Will I like the research?** (Focus)
3. **Can this person actually help me?** (Evidence)

## 5. What matters most? (Weighted Scoring)
Not every category carries the same weight. We use a "Weighted Average" to reflect what’s most important:
- **Position (45%)**: This is the big one. Even the best supervisor in the world isn't a match if they don't have a role available.
- **Focus (35%)**: You're spending 4 years on this; the research area has to be a great fit.
- **Evidence (20%)**: This is our "confidence booster." It proves the match works on a technical level, but it’s slightly less critical than the position itself.

## 6. Solving Data Quality Puzzles

### 6.1 Avoiding the "Wrong Person" trap (6.1)
**The Problem**: Searching for "Wei Wang" might find a Psychologist when you need an AI expert.
**Our Solution (Three-Layer Defense)**:
1. **Topic Filters**: We use the API's own filters to only fetch people already categorized in the right field (like "Computer Science").
2. **Focus Check**: Our first AI pass compares the supervisor's broad field to the student's intent. If it's a domain mismatch, they're rejected.
3. **Evidence Check**: Our second AI pass looks at the *actual titles* of recent papers. If the technical overlap isn't there, they're gone.

### 6.2 Finding actual supervisors, not fellow students (6.2)
**The Problem**: Sometimes PhD students or early-career researchers appear in results, but they can't actually hire you.
**Our Solution**:
- **Seniority Counts**: We only look for researchers with at least 10 publications (`IS_PI_THRESHOLD`). 
- **Role Check**: we prioritize "Contact PIs" from grant databases and official job postings. These are clear signs someone has the authority to hire.

### 6.3 Focusing on the future, not the past (6.3)
**The Problem**: A student who used to study "Plant Genetics" might keep seeing genetics ads even if they now want to study "AI."
**Our Solution (Intent Prioritization)**:
- In the "Builder" phase, we explicitly tell the AI to prioritize the student's **current research interests** over their historical background. This keeps the search looking forward.

## 7. Known Limitations

### 7.1 The "Home Student" hurdle (6.4)
**The Limitation**: While we filter by **Country**, many ads have hidden rules about citizenship (like "UK Home Students Only"). Our AI isn't perfect at catching these in long, free-text descriptions yet.
- **Our Approach**: We use strict geographic filters to get the location right, but we still advise students to double-check the funding rules in the provided links.
