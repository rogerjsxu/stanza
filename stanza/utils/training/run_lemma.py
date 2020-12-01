"""
This script allows for training or testing on dev / test of the UD tokenizer.

If run with a single treebank name, it will train or test that treebank.
If run with ud_all or all_ud, it will iterate over all UD treebanks it can find.

Args are given as follows:

python run_tokenizer.py [mode] <treebank> [tokenizer args...]

The first argument, mode, is optional.  It can either be --train (or
nothing) to train a model and report the dev score, --score_dev to
just report the dev score, or --score_test to report the test score.

After specifying the treebank, any further arguments will be passed to the tokenizer.
"""

import logging

from stanza.models import identity_lemmatizer
from stanza.models import lemmatizer

from stanza.utils.training import common
from stanza.utils.training.common import Mode

logger = logging.getLogger('stanza')

def run_treebank(mode, paths, treebank, short_name, extra_args):
    short_language = short_name.split("_")[0]

    lemma_dir      = paths["LEMMA_DATA_DIR"]
    train_file     = f"{lemma_dir}/{short_name}.train.in.conllu"
    dev_in_file    = f"{lemma_dir}/{short_name}.dev.in.conllu"
    dev_gold_file  = f"{lemma_dir}/{short_name}.dev.gold.conllu"
    dev_pred_file  = f"{lemma_dir}/{short_name}.dev.pred.conllu"
    test_in_file   = f"{lemma_dir}/{short_name}.test.in.conllu"
    test_gold_file = f"{lemma_dir}/{short_name}.test.gold.conllu"
    test_pred_file = f"{lemma_dir}/{short_name}.test.pred.conllu"
    
    if short_language in ('vi', 'fro', 'th'):
        if mode == Mode.TRAIN or mode == Mode.SCORE_DEV:
            train_args = ["--data_dir", lemma_dir,
                          "--train_file", train_file,
                          "--eval_file", dev_in_file,
                          "--output_file", dev_pred_file,
                          "--gold_file", dev_gold_file,
                          "--lang", short_name]
            logger.info("Running identity lemmatizer for {} with args {}".format(treebank, train_args))
            identity_lemmatizer.main(train_args)
        elif mode == Mode.SCORE_TEST:
            train_args = ["--data_dir", lemma_dir,
                          "--train_file", train_file,
                          "--eval_file", test_in_file,
                          "--output_file", test_pred_file,
                          "--gold_file", test_gold_file,
                          "--lang", short_name]
            logger.info("Running identity lemmatizer for {} with args {}".format(treebank, train_args))
            identity_lemmatizer.main(train_args)            
    else:
        if mode == Mode.TRAIN:
            if treebank in ('UD_Czech-PDT', 'UD_Russian-SynTagRus', 'UD_German-HDT'):
                num_epochs = "30"
            else:
                num_epochs = "60"

            train_args = ["--data_dir", lemma_dir,
                          "--train_file", train_file,
                          "--eval_file", dev_in_file,
                          "--output_file", dev_pred_file,
                          "--gold_file", dev_gold_file,
                          "--lang", short_name,
                          "--num_epoch", num_epochs,
                          "--mode", "train"]
            train_args = train_args + extra_args
            logger.info("Running train lemmatizer for {} with args {}".format(treebank, train_args))
            lemmatizer.main(train_args)

        if mode == Mode.SCORE_DEV or mode == Mode.TRAIN:
            dev_args = ["--data_dir", lemma_dir,
                        "--eval_file", dev_in_file,
                        "--output_file", dev_pred_file,
                        "--gold_file", dev_gold_file,
                        "--lang", short_name,
                        "--mode", "predict"]
            dev_args = dev_args + extra_args
            logger.info("Running dev lemmatizer for {} with args {}".format(treebank, dev_args))
            lemmatizer.main(dev_args)

        if mode == Mode.SCORE_TEST:
            test_args = ["--data_dir", lemma_dir,
                         "--eval_file", test_in_file,
                         "--output_file", test_pred_file,
                         "--gold_file", test_gold_file,
                         "--lang", short_name,
                         "--mode", "predict"]
            test_args = test_args + extra_args
            logger.info("Running test lemmatizer for {} with args {}".format(treebank, test_args))
            lemmatizer.main(test_args)

def main():
    common.main(run_treebank, "lemma", "lemmatizer")

if __name__ == "__main__":
    main()
