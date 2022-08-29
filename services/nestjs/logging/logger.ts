import { createLogger, format, transports, addColors } from 'winston';
const { combine, timestamp, printf } = format;
import { ILogger } from 'src/interfaces/ILogger';

const colorizer = format.colorize();

const logLevels = {
  levels: {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    debug: 4,
  },
  colors: {
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    debug: 'blue',
  },
};

addColors(logLevels.colors);

const logger = createLogger({
  format: combine(
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    printf((info: ILogger) => {
      const { timestamp, level, message, data, status } = info;

      return colorizer.colorize(
        level,
        `[${level.toUpperCase()}] ${
          status ? `| [STATUSCODE ${status}]` : ''
        } | [${timestamp}] | ${message} ${
          data ? `| ${JSON.stringify(data)}` : ''
        }`,
      );
    }),
  ),
  levels: logLevels.levels,
  transports: [
    new transports.Console({
      level: 'debug',
    }),
  ],
});

export default logger;
