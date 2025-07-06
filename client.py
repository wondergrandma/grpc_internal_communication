import grpc
import protos.scraper_pb2_grpc as pb2_grpc
import protos.scraper_pb2 as pb2

class Client(object):
    def __init__(self):
        self.host = "localhost"
        self.server_port = "50051"

        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = pb2_grpc.ScraperStub(self.channel)

    def test(self, message):
        message = pb2.Request(filmName=message)
        return  self.stub.ScrapeFilmInfo(message)
    
if __name__ == "__main__":
    client = Client()
    result = client.test(message="HelloWorld")
    print(f"[Client] Got response: {result.scraped}")
