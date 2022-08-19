const { createLogger, format, transports } = require('winston');
const { combine, timestamp, printf } = format;

const COLOR: any = {
  debug: '\x1b[1;38m',
  info: '\x1b[1;34m',
  error: '\x1b[1;31m',
  warn: '\x1b[1;33m',
  critical: '\x1b[1;41m',
};

const logger = createLogger({
  format: combine(
    format.align(),
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    printf(
      (info: any) =>
        `${COLOR[info.level]}${info.level.toUpperCase()}\x1b[0m | ${
          info.timestamp
        } : ${info.message}`,
    ),
  ),
  transports: [
    new transports.Console({
      prettyPrint: true,
      colorize: true,
      timestamp: true,
    }),
  ],
});

export default logger;
