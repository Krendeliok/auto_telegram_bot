FROM node:24

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install

COPY . ./

EXPOSE 3000