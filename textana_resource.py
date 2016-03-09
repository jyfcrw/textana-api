"""
API resource for text analysis (industry classification, entity matching and marked-up version of text).
"""

from flask_restful import reqparse
from flask import jsonify
from flask.ext.restful import Resource
from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS
import koltextana


class TextAnalysisResource(Resource):
    """API resource class for text analysis."""

    def __init__(self, text_analyzer):
        """Initialize Flask argument parser and text analyzers."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text', help='Marketing text to analyze')
        self.text_analyzer = text_analyzer

    def build_result(self, input_para):
        """Analyze the input text."""
        result = {}
        text = input_para["text"]
        #result = self.text_analyzer.analyze(text)
        result["industries"] = self.text_analyzer.topics(text)
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

    def get(self, input_para=None):
        """Parse arguments and build result if no errors in input"""
        result = {}
        if not input_para:
            input_para = self.parser.parse_args(strict=False)
        result["input_para"] = input_para
        errors = self.get_errors(input_para)
        if errors:
            result["errors"] = errors
        else:
            result["data"] = self.build_result(input_para)
            result["success"] = True
        print(result)
        result = jsonify(result)
        return result

    def post(self, input_para=None):
        result = {}
        if not input_para:
            input_para = self.parser.parse_args(strict=False)
        result["input_para"] = input_para
        errors = self.get_errors(input_para)
        if errors:
            result["errors"] = errors
        else:
            result["data"] = self.build_result(input_para)
            result["success"] = True
        print(result)
        result = jsonify(result)
        return result


WEB_PATH = '/kol/v1.0/text_analysis'


def run_api():
    app = Flask(__name__)
    cors = CORS(app)
    api = Api(app)
    text_analyzer = koltextana.TextAnalyzer(language="english")
    api.add_resource(TextAnalysisResource, WEB_PATH, resource_class_args=(text_analyzer,))
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    run_api()
