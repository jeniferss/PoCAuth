import { Request, Response, NextFunction } from "express";
import { Injectable, NestMiddleware } from "@nestjs/common";
import logger from "./logger";

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(request: Request, response: Response, next: NextFunction): void {
    const { ip, method, url } = request;

    response.on("finish", () => {
      const { statusCode } = response;
      logger.http(`${ip} ${method} ${url}`, {status: statusCode});
    });

    next();
  }
}
