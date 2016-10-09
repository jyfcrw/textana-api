"""
API resource for text analysis (industry classification, concept extraction and marked-up version of text).
"""

from flask_restful import reqparse
from flask import jsonify
from flask import Flask
from flask_restful import Api
import koltextana

from flask.ext.restful import Resource
from flask.ext.cors import CORS
import operator

from readability    import Readability
from urllib.request import urlopen

def infer_industries(entities):
    inferred_industries = {}
    if "producttypes" in entities and entities["producttypes"]:
        for producttype in entities["producttypes"]:
            try:
                if "core_product_of_industry" in entities["producttypes"][producttype]:
                    industry = entities["producttypes"][producttype]["core_product_of_industry"]
                    inferred_industries[industry] = producttype
            except: pass
    return inferred_industries


def format_predictions(predictions):
    """
    Predictions sorted by probability:
    {"industry": <industry(str)>, "probability": <probability(float)>}.
    """
    output = []
    for prediction in predictions:
        formatted = {"label": prediction["label"],
                     "probability": "%.3f%%" % (float(prediction["probability"]) * 100)}
        output.append(formatted)
    return output


class KoltextanaResource(Resource):
    """API resource class for text analysis."""
    def __init__(self, text_analyzer):
        """Initialize Flask argument parser and text analyzers."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text', help='Marketing text to analyze', action="append")
        self.parser.add_argument('url',  help='Marketing url  to analyze', action="append")
        self.text_analyzer = text_analyzer

    def get(self, input_para=None):
        """Parse arguments and build result if no errors in input."""
        result = {}
        if not input_para:
            input_para = self.parser.parse_args(strict=False)
        result["input_para"] = input_para

        if "text" in input_para and isinstance(input_para["text"], list) and len(input_para["text"]) == 1:
            input_para["text"] = input_para["text"][0]

        if "url" in input_para and isinstance(input_para["url"], list) and len(input_para["url"]) == 1:
            input_para["url"] = input_para["url"][0]

        errors = self.get_errors(input_para)
        if errors:
            result["errors"] = errors
        else:
            result["data"] = self.build_result(input_para)
            result["success"] = True
        result = jsonify(result)
        return result

    def get_errors(self, input_para):
        """Check for input errors."""
        errors = []
        if not input_para["text"]:
            code = "4xx"
            name = "MissingInputArgument"
            description = "Please specify a value for 'text'."
            errors.append({"code": str(code),
                           "name": name,
                           "description": description})
        return errors

    def post(self, input_para=None):
        return self.get(input_para)

    def build_result(self, input_para):
        pass


class TextAnalysisResource(KoltextanaResource):
    """API resource class for text analysis."""

    def build_result(self, input_para):
        """Analyze the input text."""
        result = {}

        if input_para["text"]:
            text = input_para["text"]
            result = self.text_analyze(text)
        elif input_para["url"]:
            article = self.text_extract(input_para["url"])
            text = article.title + " " + article.content
            result = self.text_analyze(text)
            result["article_text"] = article.content
            result["article_title"] = article.title

        result["industries"] = format_predictions(result["industries"])
        result["inferred_industries"] = infer_industries(result['entities'])
        return result

    def text_analyze(self, text):
        return self.text_analyzer.analyze(text)

    def text_extract(self, url):
        html = urlopen(url).read().decode('utf-8')
        return Readability(html, url)

    def get_errors(self, input_para):
        """Check for input errors."""
        errors = []
        if not input_para["text"] and not input_para["url"]:
            code = "4xx"
            name = "MissingInputArgument"
            description = "Please specify a value for 'text' or 'url'."
            errors.append({"code": str(code),
                           "name": name,
                           "description": description})
        return errors


class ConceptsResource(KoltextanaResource):
    """API resource class for concept extraction."""
    def build_result(self, input_para):
        """Analyze the input text."""
        text = input_para["text"]
        result = self.text_analyzer.concepts(text)
        return result


class ClassifyResource(KoltextanaResource):
    """API resource class for classification."""
    def build_result(self, input_para):
        """Analyze the input text."""
        text = input_para["text"]
        result = self.text_analyzer.topics(text)
        return result


class TopicListResource(KoltextanaResource):
    """API resource class for info about available topics."""
    def get(self, input_para=None):
        """Parse arguments and build result if no errors in input."""
        result = {}
        result["data"] = {"topics": self.text_analyzer.industry_dict}
        result["success"] = True
        result = jsonify(result)
        return result

    def post(self, input_para=None):
        return self.get()


URL_PREFIX = '/kol/v1.0/'

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
#text_analyzer = koltextana.TextAnalyzer(language="english")
text_analyzer = koltextana.TextAnalyzer(language="chinese", analyze_sentiment=True, with_markup=True)
api.add_resource(TextAnalysisResource, URL_PREFIX + "analyze", resource_class_args=(text_analyzer,))
api.add_resource(ClassifyResource, URL_PREFIX + "classify", resource_class_args=(text_analyzer,))
api.add_resource(ConceptsResource, URL_PREFIX + "concepts", resource_class_args=(text_analyzer,))
api.add_resource(TopicListResource, URL_PREFIX + "list_topics", resource_class_args=(text_analyzer,))


def run_api():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    run_api()
