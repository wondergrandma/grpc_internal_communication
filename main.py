from concurrent import futures

import grpc

from server.protos import scraper_pb2 as pb2
from server.protos import scraper_pb2_grpc as pb2_grpc
from server.scraper.tmdb_scraper import TmdbScraper


class Server(pb2_grpc.ScraperServicer):
    def __init__(self):
        self.tmdbScraper: TmdbScraper = TmdbScraper()

    def ScrapeFilmInfo(self, request, context):
        film: str = request.filmName

        result = self.tmdbScraper.scrape(searched_film=film)

        return pb2.Response(scraped=result)



def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ScraperServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    start()
