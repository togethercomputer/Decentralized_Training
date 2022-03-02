import numpy as np
from tasks.base import rf
from tasks.metrics import mean
from .common import HFTask


class CBTBase(HFTask):
    """The Children’s Book Test (CBT) from the paper:
    https://research.fb.com/wp-content/uploads/2016/11/the_goldilocks_principle_reading_children_s_books_with_explicit_memory_representations.pdf
    NOTE: This evaluation is based on the (context + query) question-answering variant
    used by the Recurrent Language Models described in the aforementioned paper.
    See section 4.4.
    """

    DATASET_PATH = "cbt"
    DATASET_NAME = None

    VERSION = 0

    def detokenize(self, text):
        text = text.replace(" '", "'")
        text = text.replace(" \n", "\n")
        text = text.replace("\n ", "\n")
        text = text.replace(" n't", "n't")
        text = text.replace("`` ", '"')
        text = text.replace("''", '"')
        # punctuation
        text = text.replace(" :", ":")
        text = text.replace(" ;", ";")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        return text

    def doc_to_text(self, doc):
        passage = " ".join(doc["sentences"])
        text = "Passage: " + passage + "\nQuestion: " + doc["question"]
        return self.detokenize(text)

    def doc_to_target(self, doc):
        return ""

    def fewshot_examples(self, k, rnd):
        assert k == 0, f"CBT is only implemented for the zero-shot setting. Given k={k}."
        return super().fewshot_examples(k, rnd)

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        lls = []
        for option in doc["options"]:
            # Following Section 4.4 "Recurrent Language Models" in the CBT paper:
            # "we rank candidate [option] c based on p(q1 . . . qk−1, c, qk+1 . . . ql)
            # rather than simply p(q1 . . . qk−1, c)."
            lls.append(rf.loglikelihood("", ctx.replace("XXXXX", option))[0])
        return lls

    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a
        dict where keys are the names of submetrics and values are the values of
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        gold = doc["options"].index(doc["answer"])
        pred = np.argmax(results)
        return {
            "acc": pred == gold
        }

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        return {
            "acc": mean
        }

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are
            whether a higher value of the submetric is better
        """
        return {
            "acc": True
        }


class CBTCN(CBTBase):
    DATASET_NAME = "CN"


class CBTNE(CBTBase):
    DATASET_NAME = "NE"
