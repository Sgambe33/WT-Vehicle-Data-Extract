import logging

logFormat = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M')

cLogger = logging.getLogger("CST-LOG")
cLogger.propagate = False

consoleHdlr = logging.StreamHandler()
consoleHdlr.setLevel(logging.INFO)

errorHdlr = logging.FileHandler('errors.log')
errorHdlr.setLevel(logging.ERROR)

cLogger.addHandler(errorHdlr)
cLogger.addHandler(consoleHdlr)

consoleHdlr.setFormatter(logFormat)
errorHdlr.setFormatter(logFormat)
