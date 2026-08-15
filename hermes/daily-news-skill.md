
# Daily News Publisher

Operate in Discovery Mode for the first 2 weeks.

## Goal
Build a broad, high-signal daily information surface. Do not over-personalize yet.

## Sections
- Today's 3
- AI / Agents
- AI Infra
- Products / Startups / Open Source
- Markets / Finance
- World / US
- For You

## Process
1. Search broadly across the last ~30 hours.
2. Collect many candidates, then deduplicate obvious repeats.
3. Prefer primary sources, official blogs, reputable reporting, technical depth, and novel products/projects.
4. In Discovery Mode, bias toward breadth. Do not suppress an unfamiliar topic just because no preference is known yet.
5. Exclude spam, SEO farms, celebrity gossip, repetitive political horse-race stories, and minor low-signal launches.
6. Generate 20–35 selected items on a normal day; hard max 40.
7. `top` is exactly 3 if 3 genuinely important stories exist.
8. `for_you` is suggestive, not authoritative; explain the hypothesis behind each recommendation.
9. Never publish private memory, private chats, credentials, employer-confidential information, or private action items.

## Item schema
Each item should include:
- title
- url
- source
- summary
- why_it_matters
- why_you_care (optional)
- badge (optional)

## Output
Write the result to `data/latest.json`, preserving the schema already in that file.
Set:
- `date`
- `generated_at`
- optional `signal`
- `meta.candidate_count`
- `meta.selected_count`

Then execute:
`./publish.sh`

After publish, send a brief WeChat DM containing:
- page URL
- top headline
- number of selected stories
Do NOT include Today's Actions on the public page.
