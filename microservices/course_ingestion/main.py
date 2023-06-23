'''Script to create a tornado server for course-ingestion'''

import tornado.ioloop
import tornado.httpserver
import config
from common.utils.logging_handler import Logger
from routes import make_app

# pylint: disable=pointless-string-statement

if __name__ == "__main__":
  app = make_app()
  if config.IS_DEVELOPMENT:
    app.listen(config.PORT)
    Logger.info(":: Starting development server on http://0.0.0.0:{}".format(
        config.PORT))
  else:
    server = tornado.httpserver.HTTPServer(app)
    server.bind(config.PORT)
    Logger.info(":: Starting production server on http://0.0.0.0:{}".format(
        config.PORT))
    server.start(1)  # forks one process per cpu
  tornado.ioloop.IOLoop.current().start()
