import pymongo
from pymongo import MongoClient
import spacy
from spacy.Summarization.v1 import Summarizer

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["researchPapers"]  # Assuming the database name from previous code

# Function to identify research trends
def identify_trends(collection_name, n_gram=1):
  """
  This function analyzes the research paper collection and identifies trends
  based on n-gram frequency in titles and abstracts.

  Args:
      collection_name (str): Name of the MongoDB collection containing papers.
      n_gram (int, optional): Number of words to consider for n-gram analysis. Defaults to 1 (unigrams).

  Returns:
      dict: Dictionary containing top n frequent n-grams and their counts.
  """
  # Fetch all documents from the collection
  papers = db[collection_name].find()

  # Initialize empty dictionary for storing n-gram counts
  ngram_counts = {}

  # Loop through each paper
  for paper in papers:
    title = paper.get("title", "")
    abstract = paper.get("summary", "")
    text = f"{title} {abstract}"  # Combine title and abstract for analysis

    # Process text and extract n-grams
    tokens = [word.lower() for word in text.split() if word.isalnum()]
    for i in range(len(tokens) - n_gram + 1):
      ngram = " ".join(tokens[i:i+n_gram])
      ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1

  # Sort n-grams by count in descending order and return top n
  top_n_grams = sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)[:10]
  return {"top_n_grams": top_n_grams}

# Function to summarize key findings of a paper
def summarize_findings(paper):
  """
  This function uses spaCy's summarization model to summarize the key findings of a paper.

  Args:
      paper (dict): A dictionary containing the paper details (title, summary, etc.)

  Returns:
      str: A summarized version of the paper's key findings.
  """
  # Load spaCy language model (ensure you have spaCy installed)
  nlp = spacy.load("en_core_web_sm")

  # Preprocess text (optional, can be improved)
  text = paper.get("content", "")  # Assuming 'content' field stores full text
  text = " ".join(word.lower() for word in text.split() if word.isalnum())
  doc = nlp(text)

  # Use spaCy summarization model
  summarizer = Summarizer(nlp)
  summary = summarizer(doc.text)
  return summary.text

# Function to generate reports based on criteria
def generate_report(criteria, collection_name):
  """
  This function generates a report based on user-defined criteria (e.g., specific keywords, publication dates).

  Args:
      criteria (dict): Dictionary containing criteria for report generation.
      collection_name (str): Name of the MongoDB collection containing papers.

  Returns:
      str: A string representation of the generated report.
  """
  # Implement logic to filter papers based on criteria and potentially use other analysis techniques
  # This part would highly depend on the specific criteria you want to support
  filtered_papers = db[collection_name].find(criteria)  # Placeholder for filtering

  # Generate report content based on the filtered papers (e.g., trends, summaries)
  report_content = ""
  for paper in filtered_papers:
    # Call functions like identify_trends or summarize_findings on each paper
    # and incorporate the results into the report content
    report_content += f"\nPaper: {paper.get('title', '')}\n"
    report_content += summarize_findings(paper)
    # ... add other analysis results

  return report_content

# Example usage
# Trend analysis
print(identify_trends("engineering_papers"))  # Replace with desired collection

# Paper summarization
paper = db["engineering_papers"].find_one()  # Fetch a sample paper
summary = summarize_findings(paper)
