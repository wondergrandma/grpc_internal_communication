import grpc
from protos import scraper_pb2_grpc as pb2_grpc
from protos import scraper_pb2 as pb2
from concurrent import futures

class Server(pb2_grpc.ScraperServicer):
    def __init__(self):
        pass

    def ScrapeFilmInfo(self, request, context):
        message = request.filmName
        print(message)

        result = {"scraped": False}

        return pb2.Response(**result)
    
def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ScraperServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    start()