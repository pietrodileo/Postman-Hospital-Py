import urllib.parse

class UrlParser:
    def __init__(self, url):
        self.url = url
        parsed_url = urllib.parse.urlparse(self.url)
        # ParseResult(scheme='http', netloc='localhost:{{port}}',
        # path='/lombardia/retelaboratori/fhir/EnsLib.REST.GenericService/',
        # params='', query='prova=prova&prova2=prova2', fragment='')
        self.url_info = {
            "raw": self.url,
            "protocol": parsed_url.scheme,
            "host": parsed_url.hostname,
            "port": parsed_url.netloc.split(":")[1],
            "path": list(filter(None, parsed_url.path.split('/'))),
            "query": []
        }
        # Parse the query string into a list of dictionaries
        query_pairs = urllib.parse.parse_qsl(parsed_url.query)
        for key, value in query_pairs:
            self.url_info["query"].append({"key": key, "value": value})