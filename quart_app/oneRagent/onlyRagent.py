import urllib.parse
import aiohttp
import xml.etree.ElementTree as ET
import logging
import asyncio

logging.basicConfig(level=logging.INFO)


async def fetch_papers(search_query):
    """
    Fetches paper details from arXiv based on a search query.

    Args:
        search_query (str): The search query string.

    Returns:
        dict or None: A dictionary containing paper details (title, summary, authors, link)
                      or None if no paper is found or an error occurs.
    """

    encoded_query = urllib.parse.quote(search_query)
    base_url = 'http://export.arxiv.org/api/query?search_query=all:'
    start_index = 0
    max_results = 1

    try:
        url = f'{base_url}{encoded_query}&start={start_index}&max_results={max_results}'
        logging.info(f'Fetching URL: {url}')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    logging.error(f'Error fetching data: HTTP {response.status}')
                    return None

                data = await response.text()
                logging.debug(f'Response data: {data}')

                try:
                    root = ET.fromstring(data)
                    entry = root.find('{http://www.w3.org/2005/Atom}entry')

                    if entry is not None:
                        # Extract details
                        paper_title = entry.find('{http://www.w3.org/2005/Atom}title').text
                        paper_summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]

                        # Find PDF link (optional)
                        pdf_link_element = entry.find('{http://www.w3.org/2005/Atom}link[@type="application/pdf"]')
                        paper_link = pdf_link_element.attrib.get('href') if pdf_link_element is not None else None

                        # Prepare paper details
                        paper_details = {
                            "title": paper_title,
                            "summary": paper_summary,
                            "authors": authors,
                            "link": paper_link
                        }
                        logging.info(f'Fetched paper details: {paper_details}')
                        return paper_details
                    else:
                        logging.warning('No entry found in XML response')
                        return None

                except ET.ParseError as e:
                    logging.error("Error parsing XML data", exc_info=True)
                    logging.error(f'Parsing error: {e}')
                    return None

    except aiohttp.ClientError as e:
        logging.error("Error fetching data", exc_info=True)
        logging.error(f'Client error: {e}')
        return None
    except asyncio.TimeoutError as e:
        logging.error("Request timed out", exc_info=True)
        logging.error(f'Timeout error: {e}')
        return None


# Example usage (assuming separate functions for each agent query)
async def eng_papers():
    search_query = "responsible AI ethics societal philosophical"
    return await fetch_papers(search_query)


async def eth_papers():
    search_query = "AI fairness bias societal impact"
    return await fetch_papers(search_query)


async def pol_papers():
    search_query = "AI policy regulation governance"
    return await fetch_papers(search_query)
