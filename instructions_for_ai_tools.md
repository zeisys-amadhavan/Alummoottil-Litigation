## START WITH THE TWO CONTROL FILES

For every substantive task concerning this legal project, begin by reading the repository's current:

1. **`README.md`** — to understand the current lay of the land: parties, proceedings, procedural posture, upcoming dates, major events, document inventory, missing records, and unresolved questions.
2. **`Strategy.md`** — to understand the objectives, strategic sequencing, plans, constraints, prohibited actions, risk controls, and current tactical priorities.

Do not assume or hard-code any case-specific objective, party, proceeding, amount, deadline, legal theory, or strategic prohibition from these Project Instructions.

**All case-specific instructions must come from `README.md` and `Strategy.md`.**

These Project Instructions are deliberately case-neutral and should work unchanged if the repository is replaced with a completely different legal matter having its own `README.md` and `Strategy.md`.

If the two files conflict:
- `README.md` controls the **current factual/procedural state**.
- `Strategy.md` controls the **objectives, constraints, sequencing and strategic choices**.
- Flag any genuine contradiction instead of silently resolving it.

## THE REPOSITORY IS THE PRIMARY RESEARCH SOURCE

The Git repository is the principal case record.

For case-specific factual, evidentiary, procedural and strategic analysis, the overwhelming majority of research should come from the repository.

As a normal working allocation:

- approximately **90–95% internal repository research**;
- approximately **5–10% external legal research**.

This ratio is a default, not a mathematical requirement. If the user specifically asks for precedent, statutory research or an external legal survey, external research may appropriately be greater.

Do not substitute Internet search results for analysis of an available internal record.

## INTERNAL RESEARCH ORDER

After reading `README.md` and `Strategy.md`, use the following source hierarchy.

### 1. Individual Markdown source documents

Search for the actual document in the repository and read its `.md` version whenever one exists.

The repository filename convention is designed to make documents discoverable. Search using combinations of:

- date;
- court / authority;
- case number;
- application / motion number;
- party;
- document type;
- subject;
- distinctive quoted wording.

Do not look for one universal `documents.md`. The **individual files themselves are the document collection**.

If the repository contains a Markdown transcription of a pleading, affidavit, objection, rejoinder, order, deed, letter, record or other source, use that document before resorting to the Binder PDF.

### 2. The complete related-document chain

Do not analyse an isolated pleading when related documents exist.

For an application or contested issue, normally locate and read as applicable:

**application / motion  
→ supporting affidavit  
→ objection / counter  
→ rejoinder / reply  
→ later affidavit or production  
→ admission application  
→ order  
→ later contradictory or explanatory records**

Search related internal analyses, chronologies, contradiction matrices, argument registries and evidence schedules where useful, but distinguish them from primary records.

### 3. Binder index

When present, use **`BINDER-TOC.md` or the repository's equivalent Binder index** as a **locator**, not as the preferred substantive source.

Its purpose is to identify:

- whether the document is in the Binder;
- Binder page or page range;
- date;
- document number;
- document identity;
- approximate page contents.

The preferred hierarchy is:

**individual `.md` document  
→ related `.md` documents  
→ `BINDER-TOC.md` locator  
→ Binder original**

Do not jump from a search question directly to hundreds of PDF pages when the repository already contains the document in Markdown.

### 4. Parsed Binder material

If an individual Markdown source does not exist or is incomplete, use any already-extracted or parsed Binder text before attempting OCR.

### 5. Original Binder image/PDF

Inspect the original scanned Binder page when visual characteristics matter, including:

- signatures;
- handwriting;
- insertions;
- strike-outs;
- overwriting;
- stamps;
- seals;
- marginal notes;
- page numbering;
- formatting;
- missing portions;
- differences between a transcription and the original.

Use `BINDER-TOC.md` first to locate the smallest relevant page range.

### 6. OCR only as the final internal resort

OCR is not the default document-reading method.

Do not OCR a scanned pleading merely because it is a PDF when a repository Markdown transcription already exists.

Use OCR only when:

1. no adequate individual Markdown source exists;
2. no adequate extracted/parsed text exists;
3. visual reading is insufficient; and
4. the information is actually necessary.

OCR only the **smallest necessary page range**.

## EXTERNAL RESEARCH COMES AFTER THE INTERNAL RECORD

For questions such as:

- what happened;
- what a party pleaded;
- what an application actually seeks;
- whether an objection was filed;
- what remains pending;
- what evidence exists;
- what a document proves;
- what procedural mistake has occurred;
- what should be done next;

begin with the internal repository, not the Internet.

Use external research mainly for matters the repository cannot itself establish, such as:

- statutory text;
- procedural rules;
- controlling precedent;
- appellate standards;
- jurisdictional law;
- limitation law;
- current court rules;
- authoritative legal interpretation.

When external research is necessary, prefer primary and authoritative sources such as legislation, official court websites and reported judgments.

External law should **test, support or refine an analysis built from the actual case record**. It should not replace that analysis.

## READ THE ACTUAL DOCUMENT BEFORE CHARACTERISING IT

Never infer the contents of a document merely from:

- its filename;
- registry description;
- README summary;
- Binder divider;
- another party's description of it;
- an earlier assistant summary.

Whenever the substance matters, read the actual source document.

For an application or motion, read the **actual prayers** before saying what relief it seeks or whether it is stale, moot, duplicative or insufficient.

For an objection, read the actual grounds.

For an order, read the operative portion and identify any trigger event for deadlines.

## RECORD FIDELITY

Never invent or silently fill missing information.

If the record does not establish something, mark it clearly as:

**QUESTION**

Maintain the following distinctions:

- **RECORD FACT** — directly established by the internal record.
- **INFERENCE / ARGUMENT** — a conclusion reasonably drawn from record facts.
- **LAW** — statute, rule or precedent.
- **QUESTION** — presently unresolved or unsupported.

Do not turn an inference into a fact.

Do not describe a document as filed merely because a draft exists.

Do not describe a document as missing merely because it was not found in the first search.

Search thoroughly before concluding that something is absent.

## VERBATIM ACCURACY

Where exact wording matters, especially for:

- sworn affidavits;
- prayers;
- judicial findings;
- admissions;
- denials;
- minutes;
- deeds;
- statutory language;

use the source wording rather than relying on memory or loose paraphrase.

If a Markdown transcription contains editorial notes, clearly distinguish those notes from the original filed text.

## STRATEGY CHECK BEFORE RECOMMENDING ACTION

Before recommending any procedural or substantive action:

1. reread the relevant part of `Strategy.md`;
2. check the current status in `README.md`;
3. read the existing pleading or application;
4. read its actual prayers;
5. read the opposing objection/counter;
6. determine whether a rejoinder/reply exists;
7. check all later developments;
8. read relevant prior orders;
9. determine whether an existing procedural vehicle already provides the needed relief;
10. identify any strategic prohibition or sequencing requirement in `Strategy.md`.

Do not recommend a new filing merely because a procedural device theoretically exists.

The strategy file decides whether additional litigation advances or damages the case plan.

## ANALYSE EXISTING VEHICLES BEFORE INVENTING NEW ONES

A recurring error in litigation analysis is to respond to a problem by proposing another application.

Before recommending a new application, amendment, proceeding or party:

- identify what existing proceedings already seek;
- determine which existing prayers remain live;
- determine whether the requested result can be obtained through an existing vehicle;
- identify the reason the existing vehicle has not produced relief;
- determine whether adding another proceeding would simply join the same queue;
- assess additional delay, service, joinder, limitation, jurisdiction and pleading risks;
- apply the priorities and prohibitions in `Strategy.md`.

Do not multiply proceedings unless the record and strategy show that a new procedural vehicle is actually necessary.

## SOURCE PRIORITY IN THE ANSWER

When both internal and external material are used, structure the reasoning in this order:

**actual internal record  
→ what that record proves or leaves unresolved  
→ applicable law  
→ strategic consequence**

Do not lead with generic legal doctrine and then attempt to fit the case into it.

## DOCUMENT MAINTENANCE

Follow whatever maintenance rules are stated in `README.md`.

Do not assume that every repository uses the same divisions or tables.

If `README.md` defines separate functions for a document registry, hearing log, chronology, status section or other structures, preserve those functions exactly.

Do not move information between sections merely because another organization seems more intuitive.

## WHEN SOURCES DISAGREE

When two internal records conflict:

- identify both;
- give the dates and source documents;
- do not silently choose one;
- determine whether the contradiction itself is legally or strategically significant;
- check `Strategy.md` for how contradictions should be treated.

## DEFAULT QUALITY STANDARD

A strong answer in this project should usually be traceable to specific internal documents.

Prefer:

**two precise internal records + the applicable rule**

over:

**ten generic web pages discussing the general subject.**

The purpose of the research process is to understand **this record**, not merely the law in the abstract.