import argparse
import json
import itertools
from collections import defaultdict

import bert_score
from bert_score import score
from rouge_score import rouge_scorer


def get_best_scores(candidates, score_list):
    per_pair_scores = defaultdict(list) 
    for cand, score in zip(candidates, score_list): 
        per_pair_scores[cand].append(score)
    best_match_scores = {cand: max(scores) for cand, scores in per_pair_scores.items()}
    return best_match_scores


def run_snippet_eval(pred_snippets, gold_snippets, debug):
    bert_scores = {}
    rouge_scores = {"rouge1": {}, "rouge2": {}, "rougel": {}}
    rscorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    for claim_id in pred_snippets:
        if claim_id not in gold_snippets:
            print(f"Warning: Claim ID {claim_id} not found in gold data - skipping!")
            continue
        if not gold_snippets[claim_id]:
            print(f"Warning: Claim ID {claim_id} has no associated evidence snippets - skipping!")
            continue

        # Generate all possible combinations of gold x predicted snippets for overlap computation
        eval_pairs = itertools.product(pred_snippets[claim_id], gold_snippets[claim_id])
        candidates, references = zip(*list(eval_pairs))

        # Compute BERT scores for all gold x predicted snippets and retain best match score per prediction
        P, R, F1 = score(candidates, references, lang='en', verbose=True)
        best_scores = get_best_scores(candidates, F1.numpy().tolist())
        mean_bert_score = sum(best_scores.values()) / len(pred_snippets[claim_id])
        bert_scores[claim_id] = mean_bert_score

        # Similarly compute ROUGE-1,2,L scores
        r1_list, r2_list, rl_list = [], [], []
        for cand, ref in zip(candidates, references):
            score_output = rscorer.score(ref, cand)
            r1_list.append(score_output['rouge1'].fmeasure)
            r2_list.append(score_output['rouge2'].fmeasure)
            rl_list.append(score_output['rougeL'].fmeasure)
        best_rouge1 = get_best_scores(candidates, r1_list)
        best_rouge2 = get_best_scores(candidates, r2_list)
        best_rougel = get_best_scores(candidates, rl_list)
        rouge_scores["rouge1"][claim_id] = sum(best_rouge1.values()) / len(pred_snippets[claim_id])
        rouge_scores["rouge2"][claim_id] = sum(best_rouge2.values()) / len(pred_snippets[claim_id])
        rouge_scores["rougel"][claim_id] = sum(best_rougel.values()) / len(pred_snippets[claim_id])
    
    # Print final score report
    final_bert_score = sum(bert_scores.values()) / len(gold_snippets)
    print(f"BERT Score: {final_bert_score}")
    final_rouge1_score = sum(rouge_scores["rouge1"].values()) / len(gold_snippets)
    print(f"ROUGE-1 Score: {final_rouge1_score}")
    final_rouge2_score = sum(rouge_scores["rouge2"].values()) / len(gold_snippets)
    print(f"ROUGE-2 Score: {final_rouge2_score}")
    final_rougel_score = sum(rouge_scores["rougel"].values()) / len(gold_snippets)
    print(f"ROUGE-L Score: {final_rougel_score}")
    # TODO: Allow dumping of per-prediction scores for analysis?

    if debug:
        json.dump(bert_scores, open("task2_bertscores.json", "w"))
        json.dump(rouge_scores, open("task2_rougescores.json", "w"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file", type=str, required=True, help="Path to prediction file")
    parser.add_argument("--gold_file", type=str, required=True, help="Path to gold data file")
    parser.add_argument("--debug", type=bool, default=False, help="Dump per-prediction scores for debuggin/analysis")
    args = parser.parse_args()

    gold_data = json.loads(open(args.gold_file).read())
    gold_snippets = {x["id"]: x["context"] for x in gold_data}

    pred_data = json.loads(open(args.pred_file).read())
    pred_snippets = {x["id"]: x["context"] for x in pred_data}

    # Run ROUGE and BERTScore evaluation for grounding snippets
    run_snippet_eval(pred_snippets, gold_snippets, args.debug)
