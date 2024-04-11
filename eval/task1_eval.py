import argparse
import json
import csv
import math
import os


def compute_dcg(pred_docs, gold_docs):
    dcg_score = 0.0
    for i, doc in enumerate(pred_docs):
        position = i + 1
        discount = 1.0 / math.log2(position + 1)
        relevance = 0.0
        if doc in gold_docs:
            # If predicted image is present in gold list, set relevance to 1.0
            relevance = 1.0
        else:
            for gdoc in gold_docs:
                # If predicted image is a sub-image or parent image of an image in gold list,
                # we set relevance to 0.5 to provide partial credit
                if doc in gdoc or gdoc in doc:
                    relevance = 0.5
                    break
        dcg_score += (discount * relevance)
    return dcg_score


def compute_idcg(relevance_ranking, rank):
    sorted_relevance_ranking = list(sorted(relevance_ranking.items(), key=lambda x: x[1], reverse=True))
    # Only consider top k relevant items for IDCG@k
    sorted_relevance_ranking = sorted_relevance_ranking[:min(len(sorted_relevance_ranking), rank)]
    idcg_score = sum([ (1.0 / (math.log2(i + 2))) * x[1] for i, x in enumerate(sorted_relevance_ranking)])
    return idcg_score


def run_eval(pred_labels, gold_labels, parse_folder, claim_citekeys, debug):
    ranks_to_eval = [5, 10]
    ndcg_scores = {n: {} for n in ranks_to_eval}
    non_empty_samples = 0

    for claim_id in pred_labels:
        if claim_id not in gold_labels:
            print(f"Warning: Claim ID {claim_id} not found in gold data - skipping!")
            continue
        if not gold_labels[claim_id]:
            print(f"Warning: Claim ID {claim_id} has no associated evidence figures/tables - skipping!")
            continue

        non_empty_samples += 1
        for rank in ranks_to_eval:
            # If #predictions < rank in predicted ranking, include all for evaluation
            pred_images = pred_labels[claim_id][:min(len(pred_labels[claim_id]), rank)]
            gold_images = gold_labels[claim_id]

            # Compute DCG score
            dcg_score = compute_dcg(pred_images, gold_images)

            # Compute ideal DCG score
            # First need to get relevance scores for all possible images
            # Images in gold list get relevance score of 1.0
            relevance_ranking = {x: 1.0 for x in gold_images}
            for file in os.listdir(os.path.join(parse_folder, claim_citekeys[claim_id])):
                if 'CAPTION' in file:
                    continue
                image_id = file.split('.png')[0]
                if image_id not in gold_images:
                    relevance_ranking[image_id] = 0.0
                    # All images that are parent/sub-images of a gold image get relevance of 0.5
                    for gold_image in gold_images:
                        if image_id in gold_image or gold_image in image_id:
                            relevance_ranking[image_id] = 0.5
                            break
            idcg_score = compute_idcg(relevance_ranking, rank)

            # Finally compute and store NDCG score@k
            ndcg_score = dcg_score / idcg_score
            ndcg_scores[rank][claim_id] = ndcg_score
    
    # Display final evaluation scores
    for rank in ranks_to_eval:
        final_ndcg = sum(list(ndcg_scores[rank].values())) / non_empty_samples
        print(f'NDCG@{rank}: {final_ndcg}')
    
    if debug:
        json.dump(ndcg_scores, open("task1_scores.json", "w"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file", type=str, required=True, help="Path to prediction file")
    parser.add_argument("--gold_file", type=str, required=True, help="Path to gold data file")
    parser.add_argument("--parse_folder", type=str, required=True, help="Path to folder containing parsed images/tables")
    parser.add_argument("--debug", type=bool, default=False, help="Dump per-prediction scores for debuggin/analysis")
    args = parser.parse_args()

    gold_data = json.loads(open(args.gold_file).read())
    gold_labels = {x["id"]: x["findings"] for x in gold_data}
    claim_citekeys = {x["id"]: x["citekey"] for x in gold_data}
    
    reader = csv.reader(open(args.pred_file))
    next(reader, None)
    pred_labels = {}
    for row in reader:
        pred_labels[row[0]] = row[1].split(',')
    
    run_eval(pred_labels, gold_labels, args.parse_folder, claim_citekeys, args.debug)