const { loadVectorStore } = require("./vectorStore");
const {
  CheerioWebBaseLoader,
} = require("langchain/document_loaders/web/cheerio");
const { RecursiveCharacterTextSplitter } = require("langchain/text_splitter");
const { neon } = require("@neondatabase/serverless");

const sql = neon(
  `postgresql://${process.env.PGUSER}:${process.env.PGPASSWORD}@${process.env.PGHOST}/${process.env.PGDATABASE}?sslmode=require`,
);

exports.train = async (dataUrls) => {
  // Ensure the trained_urls table exists
  await sql(
    `CREATE TABLE IF NOT EXISTS trained_urls (url TEXT UNIQUE NOT NULL)`,
  );
  const trainingResult = [];
  // Initialize a NeonPostgres instance to store embedding vectors
  const vectorStore = await loadVectorStore();
  try {
    const executeAsyncOperation = (element) => {
      return new Promise(async (resolve) => {
        try {
          const result = await sql(
            `SELECT COUNT(*) FROM trained_urls WHERE url = $1`,
            [element],
          );
          if (result[0].count > 0) return resolve();
          // Load LangChain's Cheerio Loader to parse the webpage
          const loader = new CheerioWebBaseLoader(element);
          const data = await loader.load();
          // Split the page into biggest chunks
          const textSplitter = new RecursiveCharacterTextSplitter({
            chunkSize: 3096,
            chunkOverlap: 128,
          });
          // Split the chunks into docs and train
          const tempSplitDocs = await textSplitter.splitDocuments(data);
          await vectorStore.addDocuments(tempSplitDocs);
          // Add to the global training array
          await sql(`INSERT INTO trained_urls (url) VALUES ($1)`, [element]);
          resolve();
        } catch (e) {
          // console.log('Faced error as below while training for', element)
          console.log(e.message || e.toString());
          console.log("Failed to train chatbot on:", element);
          trainingResult.push({ name: element, trained: false });
        }
      });
    };
    await Promise.all(
      dataUrls.map((element) => executeAsyncOperation(element)),
    );
  } catch (e) {
    console.log(e.message || e.toString());
  }
};
