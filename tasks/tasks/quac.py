"""
QuAC: Question Answering in Context
https://arxiv.org/abs/1808.07036 

@article{choi2018quac,
  title={Quac: Question answering in context},
  author={Choi, Eunsol and He, He and Iyyer, Mohit and Yatskar, Mark and Yih, Wen-tau and Choi, Yejin and Liang, Percy and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv:1808.07036},
  year={2018}
}
"""

import json
import os
from tasks.base import Task
from ..utils import sh


class QuAC(Task):
    VERSION = 0

    def __init__(self):
        super().__init__()

    def download(self):
        if not os.path.exists('data/quac'):
            # TODO: convert to use best_download
            sh("""
                mkdir -p data/quac 
                wget https://s3.amazonaws.com/my89public/quac/train_v0.2.json -O data/quac/train_v0.2.json
                wget https://s3.amazonaws.com/my89public/quac/val_v0.2.json -O data/quac/val_v0.2.json
                """)

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return False

    def training_docs(self):
        myjson = json.load(open('data/quac/train_v0.2.json'))['data']
        return self.load_doc(myjson)

    def validation_docs(self):
        myjson = json.load(open('data/quac/val_v0.2.json'))['data']    
        return self.load_doc(myjson)

    def test_docs(self):
        raise NotImplementedError("QuAC has no test docs.")
    
    def load_doc(self, myjson):
        docs = []
        for item in myjson:
            title = item['title'] + ' - ' + item['section_title']
            paragraph = item['paragraphs'][0]['context'].replace("CANNOTANSWER", "")
            qas = item['paragraphs'][0]['qas']
            qa_pairs = [(qa['question'], qa['answers'][0]['text']) for qa in qas]
            for (question, answer) in qa_pairs:
                doc = { 'title': title, 'paragraph': paragraph, 'question': question, 'answer': answer }
                docs.append(doc)  
        return docs
    
    def doc_to_text(self, doc):
        return 'TITLE: ' + doc['title'] + '\n' + 'PARAGRAPH: ' + doc['paragraph'] + '\n\n' + 'Q: ' + doc['question'] + '\n\n' + 'A: '

    def doc_to_target(self, doc):
        return doc['answer']

    def construct_requests(self, doc, ctx):
        """ Uses RequestFactory to construct Requests and returns an iterable of 
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural 
            language description, as well as the few shot examples, and the question
            part of the document for `doc`. 
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')
    
    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a 
        dict where keys are the names of submetrics and values are the values of 
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are 
            functions that aggregate a list of metrics
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are 
            whether a higher value of the submetric is better
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')
