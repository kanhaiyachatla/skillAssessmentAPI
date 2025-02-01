from serpapi import GoogleSearch

params = {
  "engine": "google_jobs",
  "q": "",
  "hl": "en",
  "api_key": "7eee66b39bc3a2fabedfc20c90fa9b891f360eb757a40ca5ed9d35390c3c1a6c"
}

search = GoogleSearch(params)
results = search.get_dict()
jobs_results = results["jobs_results"]
print(jobs_results)