# Email Scraper

This script is designed to scrape websites for contact email addresses by analyzing various elements on both the main page and the contact page. It utilizes BeautifulSoup for HTML parsing and Selenium for handling JavaScript-rendered content.
## Requirements

Ensure you have the following dependencies installed:

```bash
pip install -r requirements.txt # OR
bash setup.sh # THEN
```
## Usage

```python
email, url = run_and_get_email("https://example.com")
print(f"Email found: {email} from {url}")
```

## Configuration

- You can modify `get_contact_page()` to add more keywords for detecting contact pages.
- Change `log()` to store logs in a file if needed.

## Limitations

- Some websites may block scraping; using Selenium with a proper user-agent can help.
- JavaScript-heavy websites might require additional handling with Selenium.
- CAPTCHA-protected pages cannot be scraped without additional handling.

