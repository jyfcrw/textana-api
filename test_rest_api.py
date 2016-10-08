import unittest
import rest_api_english
import time


class TestAPIQueries(unittest.TestCase):
    TESTDATA = {"single": "I bought a car by Volkswagen.",
                "minibatch": ["I bought a car by Volkswagen.",
                                           "The movie is starring Audrey Hepburn in the lead role."],
                "1000_batch": open("testdata_english.txt", "r").readlines()
    }

    # queries taking text arguments for analysis
    ANALYSIS_QUERIES = ["classify", "concepts", "analyze"]

    #queries providing info about data model
    DATAMODEL_QUERIES = ["list_topics"]

    def setUp(self):
        rest_api_english.app.testing = True
        self.app = rest_api_english.app.test_client()

    def test_responds_to_queries(self):
        result = self.app.post(rest_api_english.URL_PREFIX+"analyze", data={"text": "BMW"})

    def test_responds_to_queries(self):
        for query in self.ANALYSIS_QUERIES:
            # single
            result = self.app.post(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["single"]})
            assert "data" in result.data.decode('utf-8')
            result = self.app.get(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["single"]})
            assert "data" in result.data.decode('utf-8')
            # batch
            result = self.app.post(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["minibatch"]})
            assert "data" in result.data.decode('utf-8')
            result = self.app.get(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["minibatch"]})
            assert "data" in result.data.decode('utf-8')

        for query in self.DATAMODEL_QUERIES:
            result = self.app.post(rest_api_english.URL_PREFIX+query, data=None)
            assert "data" in result.data.decode('utf-8')
            result = self.app.get(rest_api_english.URL_PREFIX+query, data=None)
            assert "data" in result.data.decode('utf-8')

    def test_batch_performance(self):
        print("Testing on %d items:" % len(self.TESTDATA["1000_batch"]))

        for query in self.ANALYSIS_QUERIES:
            start = time.time()
            _ = self.app.post(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["1000_batch"]})
            end = time.time()
            elapsed = abs(start - end)
            print("POST/%s: %s" % (query, str(elapsed)))

            start = time.time()
            _ = self.app.get(rest_api_english.URL_PREFIX+query, data={"text": self.TESTDATA["1000_batch"]})
            end = time.time()
            elapsed = abs(start - end)
            print("GET/%s: %s" % (query, str(elapsed)))


if __name__ == "__main__":
    unittest.main()
