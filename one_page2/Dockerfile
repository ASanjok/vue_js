# start with node image
FROM node:18 AS build-stage

# work directory
WORKDIR /app


COPY package*.json ./

# Install dependencies
RUN npm install

# copy full project
COPY . .

# build app
RUN npm run build

# use nginx server
FROM nginx:alpine AS production-stage

# copy komiled app in to nginx dir
COPY --from=build-stage /app/dist /usr/share/nginx/html


EXPOSE 80

# start nginx
CMD ["nginx", "-g", "daemon off;"]
