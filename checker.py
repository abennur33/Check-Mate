from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

from fact_checking import FactChecker

import sys


def get_confidence(context, claim):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact_checker = FactChecker(fact_checking_model, tokenizer)
    is_claim_true = fact_checker.validate_with_replicas(context, claim)
    return is_claim_true['Y'] * 100
