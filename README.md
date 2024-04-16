# Context24: Dataset repository for SDPROC Shared Task: Context24: Contextualizing Scientific Figures and Tables

This repository hosts the training/dev datasets and evaluation scripts for the [2024 Workshop on Scholarly Document Processing](https://sdproc.org/2024/sharedtasks.html#context24) Shared Task: **Context24: Contextualizing Scientific Figures and Tables**

## Dataset and directory structure

The claims and papers from this task come from four separate datasets, each of which comes from a different set of research domains.
1. `akamatsulab`: Cell biology
2. `BIOL403`: Cell biology
3. `dg-social-media-polarization`: Social sciences (political science, economics, HCI)
4. `megacoglab`: Various (HCI, psychology, economics, CS, public health)

The directory structure is as follows:
```
task1-train-dev.json
task2-train-dev.json
fulltexts.json
figures-tables/
	citekey/
		FIG 1.png
		...
silver-data/
eval/
```

The main training/dev datasets are in `task1-train-dev.json` and `task2-train-dev.json`.

Parsed figures, tables, and captions for each paper, as `.png` files, are in `figures-tables`, organized by paper citekey as enclosing subfolders.

Full-text parses for each paper are in `fulltexts.json`.

Evaluation scripts for each task are in `eval/`

As an additional possibly useful resource, `silver-data` contains full text parses for 17,007 papers from 1-2 hop in-bound and out-bound citations of the focal papers. 

## Task 1: Evidence Identification

### Task description

Given a scientific claim and a relevant research paper, predict a shortlist of key figures or tables from the paper that provide supporting evidence for the claim.

Here is an example claim with a Figure as its key supporting evidence.

```
{
	"id": "akamatsulab-WJvOy9Exn",
	"claim": "The density of free barbed ends increased as a function of growth stress",
	"citekey": "li2022molecular",
	"dataset": "akamatsulab",
	"findings": [
		"FIG 1D"
	]
}
```

And an example claim with a Figure and Table as its key supporting evidence.

```
{
	"id": "dg-social-media-polarization-tQy4sEF_R",	
	"claim": "Perceived polarization increased as a function of time spent reading a tweet, but only for Republican users",
	"citekey": "banksPolarizedFeedsThreeExperiments2021",
	"dataset": "dg-social-media-polarization",
	"findings": [
		"FIG 6",
		"TAB 2"
	]
}
```

Each claim corresponds to a paper via the `citekey` field. The figures, tables, and captions for that paper can be found in the `figures-tables/` , under the subfolder with the same name as the `citekey`. The figures, tables, and captions are a set of `.png` files.

Scoring will be done using NDCG at 5 and 10. More details in `eval1.py` in `eval/`.

### Training and dev data description

There are currently 393 total scientific claims across the four datsets, in the following breakdown

| Dataset                      | N   |
| ---------------------------- | --- |
| akamatsulab                  | 166 |
| BIOL403                      | 29  |
| dg-social-media-polarization | 76  |
| megacoglab                   | 122 |

Approximately 100 more are forthcoming by ~April 19.

## Task 2: Grounding Context Identification

### Task description

Given a scientific claim and a relevant research paper, identify all grounding context from the paper discussing methodological details of the experiment that resulted in this claim. For the purposes of this task, grounding context is restricted to quotesa from the paper. These grounding context quotes are typically dispersed throughout the full-text, often far from where the supporting evidence is presented. 

For maximal coverage for this task, search for text snippets that cover the following key aspects of the empirical methods of the claim:
1. **What** observable measures/data were collected
2. **How** (with what methods, analyses, etc.) from
3. **Who**(m) (which participants, what dataset, what population, etc.)

_NOTE_: we will not be scoring the snippets separately by context "category" (e.g. who/how/what): we provide them here to clarify the requirements of the task.

Here is an example claim with a quotes as empirical methods context.

```
{
    "id": "megacoglab-W3sdOb60i",
    "claim": "US patents filed by inventors who were new to the patent's field tended to be more novel",
    "citekey": "artsParadiseNoveltyLoss2018a",
    "dataset": "megacoglab",
    "context": [
        "To assess patent novelty, we calculate new combinations (ln) as the logarithmic transformation of one plus the number of pairwise subclass combinations of a patent that appear for the first time in the US. patent database (Fleming et al. 2007, Jung and Jeongsik 2016). To do so, each pairwise combination of subclasses is compared with all pairwise combinations of all prior U.S. patents. (p. 5)",
        "we begin with the full population of inventors and collect all patents assigned to \ufb01rms but, by design, must restrict the sample to inventors who have at least two patents assigned to the same \ufb01rm. The advantage of this panel setup is that we can use inventor\u2013firm fixed effect models to control for unobserved heterogeneity among inventors and firms, which arguably have a strong effect on the novelty and value of creative output. This approach basically uses repeated patents of the same inventor within the same firm to identify whether the inventor creates more or less novel\u2014and more or less valuable\u2014patents when any subsequent patent is categorized in a new \ufb01eld. The sample includes 2,705,431 patent\u2013inventor observations assigned to 396,336 unique inventors and 46,880 unique firms, accounting for 473,419 unique inventor\u2013firm pairs. (p. 5)",
        "For each inventor-patent observation, we retrieve the three-digit technology classes of all prior patents of the focal inventor and identify whether there is any overlap between the three-digit technology classes of the focal patent and the three-digit technology classes linked o all prior patents of the same inventor. We rely on all classes assigned to a patent rather than just the primary class. Exploring new fields is a binary indicator that equals one in the absence of any overlapping class between all prior patents and the focal patent. (p. 6)",
        "we can use inventor\u2013\ufb01rm \ufb01xed effect models to control for unobserved heterogeneity among inventors and \ufb01rms, which arguably have a strong effect on the novelty and value of creative output (p. 5)",
        "we select the full population of inventors with U.S. patents assigned to \ufb01rms for 1975\u20132002 (p. 3)"
    ]
  },
```

In this example, the quotes fall into the following aspects of empirical methods:

**What**: 
> "To assess patent novelty, we calculate new combinations (ln) as the logarithmic transformation of one plus the number of pairwise subclass combinations of a patent that appear for the first time in the US. patent database (Fleming et al. 2007, Jung and Jeongsik 2016). To do so, each pairwise combination of subclasses is compared with all pairwise combinations of all prior U.S. patents. (p. 5)"
> 
> "For each inventor-patent observation, we retrieve the three-digit technology classes of all prior patents of the focal inventor and identify whether there is any overlap between the three-digit technology classes of the focal patent and the three-digit technology classes linked o all prior patents of the same inventor. We rely on all classes assigned to a patent rather than just the primary class. Exploring new fields is a binary indicator that equals one in the absence of any overlapping class between all prior patents and the focal patent. (p. 6)"

**Who**:
> "we select the full population of inventors with U.S. patents assigned to \ufb01rms for 1975\u20132002 (p. 3)"

**How**:
> "we begin with the full population of inventors and collect all patents assigned to \ufb01rms but, by design, must restrict the sample to inventors who have at least two patents assigned to the same \ufb01rm. The advantage of this panel setup is that we can use inventor\u2013firm fixed effect models to control for unobserved heterogeneity among inventors and firms, which arguably have a strong effect on the novelty and value of creative output. This approach basically uses repeated patents of the same inventor within the same firm to identify whether the inventor creates more or less novel\u2014and more or less valuable\u2014patents when any subsequent patent is categorized in a new \ufb01eld. The sample includes 2,705,431 patent\u2013inventor observations assigned to 396,336 unique inventors and 46,880 unique firms, accounting for 473,419 unique inventor\u2013firm pairs. (p. 5)"

> "we can use inventor\u2013\ufb01rm \ufb01xed effect models to control for unobserved heterogeneity among inventors and \ufb01rms, which arguably have a strong effect on the novelty and value of creative output (p. 5)"

Scoring will be done using ROUGE and BERT score similarity to the gold standard quotes. See `eval2.py` in `eval/` for more details.

### Example test data

Task 2 is a "test-only" task. In liueu of training data, we are releasing a small (N=42) set of examples, which can be used to get an idea for the task, with the following breakdown across the `akamatsulab` and `megacoglab` datasets:

| Dataset                      | N   |
| ---------------------------- | --- |
| akamatsulab                  | 28 |
| megacoglab                   | 14 |
