const { question } = require("./ask");
const { scrapeWebsite } = require("./scrape");

scrapeWebsite("https://rishi.app").then(() => {
  question("How do you use service worker with Vue 3?");
});
