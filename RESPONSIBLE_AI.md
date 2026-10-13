# Responsible AI
This document describes how the AI Q&A feature in this project was built with responsible AI practices in mind, and is honest about what it does and doesn't do well.

## Hallucination
The AI feature is grounded in real data rather than answering from general knowledge. When a question is asked, the system retrieves the data currently filtered on the dashboard (via the existing indicator/country/year selectors), passes it to the model as evidence alongside the question, and instructs the model to answer only from that evidence and admit when the data doesn't support an answer. This was tested against four categories of questions: a direct data lookup, a calculation, a question about data outside the current selection, and a completely unrelated question — in each case the system behaved correctly rather than inventing an answer.

## Bias
This project uses only 4 countries (Jordan, Egypt, Lebanon, Saudi Arabia), chosen for relevance rather than statistical representativeness. Any comparison or trend shown is only true relative to these specific countries, not the region or world broadly, and choosing different comparators could change the impression given. The underlying data also comes from government-reported national statistics (via WDI and Jordan’s DOS); different countries can measure the same indicator (e.g. unemployment) with different methodologies, and governments can have an incentive to report favorable figures. These are systematic, structural skews, not random errors, and are known limitations of this kind of data rather than something specific to this project.

## Data quality
Data quality issues (missing years, staggered indicator coverage, a UTF-8 BOM bug, etc.) are documented in `data_notes.md` and in the dashboard's own Sources and Methodology section. Those same limitations apply to any answer the AI feature gives, since it answers from the same underlying data. If the chart/table has a gap, the AI's evidence has the same gap.

## Privacy
All data used is aggregate, country- or governorate-level statistics (e.g. national unemployment rates, poverty rates) sourced from public institutions (World Bank, UNDP, Jordan's Department of Statistics). No individual-level or personally identifiable data is collected, stored, or processed anywhere in this project.

## Transparency
The AI feature is not a black box: it does not use embeddings or semantic search. It works by taking whatever data is currently filtered on the dashboard, converting it to a plain CSV table, and sending that table plus the user's question to the Gemini API with instructions to answer only from that data. A visible disclaimer in the app tells users the answer is AI-generated and should be treated as a starting point, not an authoritative source.

## Limitations
- **Arithmetic reliability**: the AI feature is not fully reliable when it comes to arithmetic. It has calculated correctly during testing, but language models are known to make mistakes with exact calculations even when the numbers are provided directly, so this should not be assumed to always be correct.
- **Scope limited to the current filter selection**: the AI only answers using the data currently filtered by the dashboard's indicator/country/year selectors, not the whole dataset. If a question is about something outside the current selection, the system will say it doesn't have enough data, even though that data may exist elsewhere in the database.
- **Instruction-following is not a hard guarantee**: the model is instructed (via its system instruction) to answer only from the given data and admit when it lacks support for an answer, but this relies on the model choosing to follow that instruction. It is not enforced by code the way the empty-question check is. There is no absolute guarantee it will behave this way on every possible question.
- **Non-deterministic output**: the model's temperature is set to 0.3, which was chosen to keep answers fairly consistent, but it does not guarantee that the exact same question will produce an identical answer every time it's asked.

## Human oversight & appropriate use
The dashboard displays a visible disclaimer alongside every AI answer: *"This answer is AI-generated from the data currently shown above. Treat it as a starting point for exploration, not an authoritative source; verify important figures against the chart/table above."* This tool is intended to help someone explore and ask quick questions about the data already shown on this dashboard. It is not intended to replace checking the original data sources, and it should not be used as the sole basis for official reporting, academic citation, or policy decisions.