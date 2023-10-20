class DataFrame:
    def __init__(self, api_method: str, test_status=None, query_list=[]):
        self.api_method = api_method
        self.query_list = query_list
        self.rank = 0
        self.passed = 1 if test_status == "passed" else 0
        self.failed = 1 if test_status == "failed" else 0
        self.broken = 1 if test_status == "broken" else 0
        self.skipped = 1 if test_status == "skipped" else 0
        # TODO
        # add weight for critical API methods
        # add status code for API