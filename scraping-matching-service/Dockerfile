# Dockerfile for scraping-matching-service
# Use Node.js image
FROM node:20

WORKDIR /usr/src/app

# Install Playwright dependencies (headless browser)
RUN apt-get update && apt-get install -y \
  gconf-service \
  libasound2 \
  libatk1.0-0 \
  libcups2 \
  libdbus-1-3 \
  libfontconfig1 \
  libgbm1 \
  libgconf-2-4 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libxss1 \
  libxtst6 \
  xdg-utils \
  libx11-xcb1 \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Playwright
COPY package*.json ./
RUN npm install
RUN npx playwright install --with-deps

COPY . .

EXPOSE 3001

CMD ["node", "src/index.js"]
