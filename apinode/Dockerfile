FROM node:18-slim

WORKDIR /app

# Copia package.json e package-lock.json (se existir)
COPY package*.json ./

# Instala os pacotes específicos primeiro (caso queira forçar essas versões)
RUN npm install express axios redis

# Instala as dependências do package.json (se houver outras)
RUN npm install

# Copia o restante do código da aplicação
COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
