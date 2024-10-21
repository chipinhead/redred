const { train } = require("./train");
const { DOMParser } = require("xmldom");

function makeURLs(xmlString) {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(xmlString, "application/xml");
  const locElements = xmlDoc.getElementsByTagName("loc");
  return Array.from(locElements).map((element) => element.textContent);
}

async function scrapeWebsite(url) {
  const callSitemap = await fetch(new URL("/sitemap.xml", url).toString());
  const responseSitemap = await callSitemap.text();
  const sitemapURLs = makeURLs(responseSitemap);
  console.log("Found", sitemapURLs.length, "urls to scrape.");
  console.log("Training...");
  await train(sitemapURLs);
  console.log("Completed training!");
}

exports.scrapeWebsite = scrapeWebsite;
