# Context24: Dataset repository for SDPROC Shared Task: Context24: Contextualizing Scientific Figures and Tables

This repository will host the training/dev datasets and evaluation scripts for the [2024 Workshop on Scholarly Document Processing](https://sdproc.org/2024/sharedtasks.html#context24) Shared Task: **Context24: Contextualizing Scientific Figures and Tables**

## Task 1: Evidence Identification
Given a scientific claim and a relevant research paper, identify key figures or tables from the paper that provide supporting evidence for the claim.

- [ ] more details to be summarized from evaluation script

Here is an example claim with a Table as its key supporting evidence.

```
{
    "id": "megacoglab-IUA1p7faR",
    "claim": "US patents in the early 90's were more likely to be exapted by inventors who had previous patent experience in the focal and-or citing patent subclasses",
    "citekey": "mastrogiorgioInnovationExaptationIts2016",
    "dataset": "megacoglab",
    "findings": {
      "Tables": [
        "Table 3",
      ],
      "Figures": [],
    },
  }
```

## Task 2: Grounding Context Identification

Given a scientific claim and a relevant research paper, identify all grounding context from the paper discussing methodological details of the experiment that resulted in this claim. This grounding context is typically dispersed throughout the full-text, often far from where the supporting evidence is presented and can include figures, tables or text snippets. 

For maximal coverage for this task, search for text snippets or figures/tables that cover the following key aspects of the empirical methods of the claim:
1. **What** observable measures/data were collected
2. **How** (with what methods, analyses, etc.) from
3. **Who**(m) (which participants, what dataset, what population, etc.)

_NOTE 1_: we will not be scoring the snippets separately by context "category" (e.g. who/how/what): we provide them here to clarify the requirements of the task.

_NOTE 2_: the dataset for Task 2 will be a "test-only" dataset: that is, we are releasing a small (~40 or so) set of examples, which can be used to get an idea for the task.

Here is an example claim with a table and text snippets as grounding context.

```
{
    "id": "megacoglab-IUA1p7faR",
    "claim": "US patents in the early 90's were more likely to be exapted by inventors who had previous patent experience in the focal and-or citing patent subclasses",
    "citekey": "mastrogiorgioInnovationExaptationIts2016",
    "dataset": "megacoglab",
    "context": {
      "Tables": [
        "Table 1"
      ],
      "Figures": [],
      "Quotes": [
        "In order to test our hypotheses, we studied exaptation at the invention level; we identified an invention with a patent and considered a cross-section of U.S. patents. Raw patent data were obtained from the USPTO and/NBER databases (Hall et al., 2001),and the main measures were built after merging these databases to the Patent Network Dataverse (Lai et al, 2011).",
        "Our empirical framework consisted of the following steps: (1) we considered a random cross-section of US. patents granted between January and June 1991 (both theJanuary-June interval and the year 1991 were chosen randomly); (2) for each patent we used a 1991-1999 window of forward citations to calculate exaptation; (3) for each patent we then considered a 1975-1990 pre-sample window in order to calculate technological complexity, inventor's analogical ability, and other controls. The estimation sample consists of 19076 patents.",
        "As our dependent variable is a proportion, we adopted the fractional logit estimation procedure proposed by Papke and Wooldridge (1996).",
        "a forward citation is cross-class if both the OX and XR classes of the focal patent differ from the OR class of the citing patent",
        "The ability of inventors to draw inventive analogies and exapt existing technologies across different domains is a function of their stock of knowledge spanning these domains. We introduced a novel measure of inventors\u2019 analogical abilities that quantifies their multi-domain skills: In order to build the measure, we considered the inventor (or team) belonging to the first citing patent. We then extracted, from the Patent Network Dataverse (Lai et al, 2011),the inventor\u2019s previous patents that belong to the 1975-1990 pre-sample window. We then counted the number of previous patents whose OR class was equal to the OR class of either the focal patent or the citing patent."
      ]
    }
  }
```
