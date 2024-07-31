import urllib.parse
import aiohttp
import xml.etree.ElementTree as ET
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO)

# MongoDB setup
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "research_papers_db"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

async def fetch_papers(search_query, collection_name):
    """
    Fetches paper details from arXiv based on a search query and stores them in MongoDB.

    Args:
        search_query (str): The search query string.
        collection_name (str): The MongoDB collection name to store the papers.
    """

    encoded_query = urllib.parse.quote(search_query)
    base_url = 'http://export.arxiv.org/api/query?search_query=all:'
    start_index = 0
    max_results = 500

    url = f'{base_url}{encoded_query}&start={start_index}&max_results={max_results}'
    logging.info(f'Fetching URL: {url}')

    try:
        async with aiohttp.ClientSession() as aio_session:
            async with aio_session.get(url, timeout=30) as response:
                if response.status != 200:
                    logging.error(f'Error fetching data: HTTP {response.status}')
                    return

                data = await response.text()
                logging.debug(f'Response data: {data}')

                try:
                    root = ET.fromstring(data)
                    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

                    papers = []

                    for entry in entries:
                        paper_title = entry.find('{http://www.w3.org/2005/Atom}title').text
                        paper_summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                        pdf_link_element = entry.find('{http://www.w3.org/2005/Atom}link[@type="application/pdf"]')
                        paper_link = pdf_link_element.attrib.get('href') if pdf_link_element is not None else None

                        paper_details = {
                            "title": paper_title,
                            "summary": paper_summary,
                            "authors": authors,
                            "link": paper_link
                        }

                        papers.append(paper_details)

                    if papers:
                        await db[collection_name].insert_many(papers)
                        logging.info(f'Successfully fetched and stored {len(papers)} papers for query: {search_query}')

                except ET.ParseError as e:
                    logging.error("Error parsing XML data", exc_info=True)
                    logging.error(f'Parsing error: {e}')
                except Exception as e:
                    logging.error("Error processing data", exc_info=True)
                    logging.error(f'Processing error: {e}')

    except aiohttp.ClientError as e:
        logging.error("Error fetching data", exc_info=True)
        logging.error(f'Client error: {e}')
    except asyncio.TimeoutError as e:
        logging.error("Request timed out", exc_info=True)
        logging.error(f'Timeout error: {e}')


# Agent functions to fetch papers for each domain
async def eng_papers():
    search_query = "engineering AI"
    await fetch_papers(search_query, "engineering_papers")

async def eth_papers():
    search_query = "ethics AI"
    await fetch_papers(search_query, "ethics_papers")

async def pol_papers():
    search_query = "policy AI"
    await fetch_papers(search_query, "policy_papers")

# Main function to run the tasks concurrently
async def main():
    tasks = [eng_papers(), eth_papers(), pol_papers()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
