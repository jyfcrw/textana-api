import unittest
import rest_api
import time

class TestAPIQueries(unittest.TestCase):
    TESTCASE = "Golf is a car by Volkswagen."

    def test_app_queries(self):
        test_queries = ["analyze", "classify", "concepts"]

        rest_api.app.testing = True
        client = rest_api.app.test_client()
        for query in test_queries:
            query_string = rest_api.WEB_PATH + '%s?text=%s' % (query, self.TESTCASE)
            # test GET requests
            self.assertEquals(str(client.get(query_string)), "<Response streamed [200 OK]>")
            # test POST requests
            self.assertEquals(str(client.post(query_string)), "<Response streamed [200 OK]>")

    def test_performance_of_app_queries(self):
        test_queries = ["analyze", "classify", "concepts"]

        rest_api.app.testing = True
        client = rest_api.app.test_client()

        argument_string = ""
        test_data = open("testdata_english.txt", "r").readlines()
        for data_item in test_data:
            argument_string += "text=%s&" % data_item.strip()

        for query in test_queries:
            query_string = rest_api.WEB_PATH + '%s?text=%s' % (query, argument_string[:-1])

            # GET
            start = time.time()
            get_response = client.get(query_string)
            end = time.time()
            elapsed = abs(start - end)
            print("GET %s on %s items: %s" % (query, str(len(test_data)), str(elapsed)))
            # POST
            start = time.time()
            post_response = client.post(query_string)
            end = time.time()
            elapsed = abs(start - end)
            print("POST %s on %s items: %s" % (query, str(len(test_data)), str(elapsed)))


if __name__ == "__main__":
    unittest.main()
