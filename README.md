# SUPER ALPHA WARNING

This is a work in progress.

## Setup Docker

The docker-compose will set up a simple python environment with the necessary dependencies, and a vector database.

1. Install Docker
2. Copy .env.dis to .env and fill in the values
3. Run `docker compose up -d`
4. Run `docker compose exec -it cli bash`
5. Run `python -m migrations.new` (you can do this to wipe you vector store whenever you want)
6. Run `python -m migrations.create` (this creates a store for the raw reddit objects)

## Pulling and storing data by date 
1. Run `python date.py --timezone="$TIMEZONE" --subreddit="$SUBREDDIT" --date="$DATE"` (this will ouput a json file to /data)
1a. Run `python search.py "$QUERY" --subreddit="$SUBREDDIT"`
2. Run `python flatten.py "$json_file"` (this will output a json file "_flat" to /data)
3. Run `COLLECTION_NAME=$collection_name python store.py "$json_file"` (this will create embeddings with openai and store the data in the vector database using  langchain and vectoredb)

## asking questions
1. Run `COLLECTION_NAME=$collection_name python ask.py "your question"` (this will output the answer in the terminal)

## example bash script to pull and store data for several subreddits and dates
```bash
#!/bin/bash

# Check if a date argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <DATE>"
  exit 1
fi

# Assign the date provided from the CLI
DATE=$1

# List of subreddits
subreddits=(
  "AI_Agents"
  "AutoGenAI"
  "ChatGPT"
  "ChatGPTPro"
  "ClaudeAI"
  "LocalLLaMA"
  "notebooklm"
  "OpenAI"
  "perplexity_ai"
  "Rag"
  "CrewAI"
  "ArtificialInteligence"
  "ChatGPTPromptGenius"
)

# Timezone
TIMEZONE="America/Los_Angeles"

# Iterate through each subreddit and run the command
for SUBREDDIT in "${subreddits[@]}"; do
  echo "Running for subreddit: $SUBREDDIT"
  python date.py --timezone="$TIMEZONE" --subreddit="$SUBREDDIT" --date="$DATE"
done
```

```bash
./ai.sh "2024-10-24"
```

## example bash script to combine storage steps 
```bash
#!/bin/bash

# Check if at least two arguments were provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <SCRIPT_NAME> <DATE_OR_QUERY> [--subreddit=SUBREDDIT]"
  exit 1
fi

SCRIPT=$1
DATE_OR_QUERY=$2
SUBREDDIT=""

# Check for optional --subreddit flag
if [[ $3 == --subreddit=* ]]; then
  SUBREDDIT=${3#*=}
fi

# Step 1: Run the specified script with the provided arguments
if [ "$SCRIPT" = "search" ]; then
  if [ -n "$SUBREDDIT" ]; then
    output=$(python search.py "$DATE_OR_QUERY" --subreddit="$SUBREDDIT")
  else
    output=$(python search.py "$DATE_OR_QUERY")
  fi
else
  output=$(./"$SCRIPT.sh" "$DATE_OR_QUERY")
fi

# Step 2: Parse JSON file paths from the output
json_files=$(echo "$output" | grep -oE '/data/[^[:space:]]+\.json')

# Step 3 & 4: Run flatten.py for each JSON file and parse the flattened file paths
for json_file in $json_files; do
  flattened_output=$(python flatten.py "$json_file")
  flattened_files=$(echo "$flattened_output" | grep -oE '/data/[^[:space:]]+_flat\.json')
  
  # Step 5: Run store.py for each flattened JSON file
  for flat_file in $flattened_files; do
    python store.py "$flat_file"
  done
done

echo "Processing complete."
```
### Example

```bash
COLLECTION_NAME=ai  ./train.sh ai "2024-10-24" --subreddit=AI_Agents
```

```bash
COLLECTION_NAME=ai  ./train.sh search "$QUERY"
```

