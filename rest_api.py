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


class KoltextanaResource(Resource):
    """API resource class for text analysis."""

    def __init__(self, text_analyzer):
        """Initialize Flask argument parser and text analyzers."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text', help='Marketing text to analyze', action="append")
        #self.parser.add_argument('texts', help='Marketing texts to analyze', action="append")
        self.text_analyzer = text_analyzer

    def get(self, input_para=None):
        """Parse arguments and build result if no errors in input."""
        result = {}
        if not input_para:
            input_para = self.parser.parse_args(strict=False)
        result["input_para"] = input_para
        if "text" in input_para and isinstance(input_para["text"], list) and len(input_para["text"]) == 1:
            input_para["text"] = input_para["text"][0]
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

    def __init__(self, text_analyzer):
        """Initialize Flask argument parser and text analyzers."""
        super(TextAnalysisResource, self).__init__(text_analyzer)

    def build_result(self, input_para):
        """Analyze the input text."""
        text = input_para["text"]
        result = self.text_analyzer.analyze(text)
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


class ConceptsResource(KoltextanaResource):
    """API resource class for concept extraction."""

    def __init__(self, text_analyzer):
        super(ConceptsResource, self).__init__(text_analyzer)

    def build_result(self, input_para):
        """Analyze the input text."""
        text = input_para["text"]
        result = self.text_analyzer.concepts(text)
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


class ClassifyResource(KoltextanaResource):
    """API resource class for classification."""

    def __init__(self, text_analyzer):
        super(ClassifyResource, self).__init__(text_analyzer)

    def build_result(self, input_para):
        """Analyze the input text."""
        text = input_para["text"]
        result = self.text_analyzer.topics(text)
        return result


class TopicListResource(KoltextanaResource):
    """API resource class for classification."""
    def __init__(self, text_analyzer):
        super(TopicListResource, self).__init__(text_analyzer)

    def build_result(self, input_para):
        """Analyze the input text."""
        result = {"topics": self.text_analyzer.industry_dict}
        return result

    def build_errors(self):
        pass


WEB_PATH = '/kol/v1.0/'

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
text_analyzer = koltextana.TextAnalyzer(language="english")

api.add_resource(TextAnalysisResource, WEB_PATH + "analyze", resource_class_args=(text_analyzer,))
api.add_resource(ClassifyResource, WEB_PATH + "classify", resource_class_args=(text_analyzer,))
api.add_resource(ConceptsResource, WEB_PATH+"concepts", resource_class_args=(text_analyzer,))
api.add_resource(TopicListResource, WEB_PATH+"topiclist", resource_class_args=(text_analyzer,))


def run_api():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    run_api()
