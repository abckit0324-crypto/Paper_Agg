from .base import EventScraper, PaperData
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class USENIXScraper(EventScraper):
    def scrape(self, url: str) -> list[PaperData]:
        papers = []
        soup = self.get_soup(url)
        if not soup:
            return papers

        # USENIX Security has two different page structures:
        # 1. "technical-sessions" pages (2022-2024): Papers are in divs with links
        # 2. "accepted-papers" pages (2025+): Papers are in a simple list
        
        # Find all links that could be papers
        # Papers typically link to paths like /conference/usenixsecurity{year}/presentation/{paper-slug}
        paper_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            # Match presentation links
            if '/presentation/' in href:
                paper_links.append(link)
        
        # Process each paper link
        for link in paper_links:
            title = link.get_text(strip=True)
            if not title:
                continue
                
            paper_url = urljoin(url, link['href'])
            
            # Try to find authors - they might be in nearby text or we skip for now
            # USENIX pages often don't show authors on the listing page
            authors = "USENIX Security Authors"
            
            papers.append(PaperData(
                title=title,
                authors=authors,
                url=paper_url,
                pdf_url=None  # PDFs are usually on the paper's individual page
            ))
        
        return papers
