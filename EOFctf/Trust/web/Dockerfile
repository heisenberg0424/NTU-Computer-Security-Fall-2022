FROM node:19-alpine

COPY src /app
WORKDIR /app
RUN yarn

ENTRYPOINT ["yarn", "start"]
