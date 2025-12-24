#!/usr/bin/env python3
"""
Complete Mutual Fund Data Scraper with Structured JSON Output
Extracts all fields from Groww.in mutual fund pages
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

ALL_FUNDS = [
    "hdfc-mid-cap-fund-direct-growth",
    "hdfc-focused-fund-direct-growth",
    "hdfc-equity-fund-direct-growth",
    "hdfc-elss-tax-saver-fund-direct-plan-growth",
    "hdfc-retirement-savings-fund-equity-plan-direct-growth",
    "hdfc-balanced-advantage-fund-direct-growth",
    "hdfc-large-cap-fund-direct-growth",
    "hdfc-i-come-plus-arbitrage-active-fof-direct-growth",
    "hdfc-short-term-opportunities-fund-direct-growth",
    "hdfc-infrastructure-fund-direct-growth",
    "hdfc-multi-cap-fund-direct-growth",
    "hdfc-small-cap-fund-direct-growth",
    "hdfc-large-and-mid-cap-fund-direct-growth",
    "hdfc-multi-asset-active-fof-direct-growth",
    "hdfc-nifty50-equal-weight-index-fund-direct-growth",
    "hdfc-banking-financial-services-fund-direct-growth",
    "hdfc-nifty-100-equal-weight-index-fund-direct-growth",
    "hdfc-nifty-next-50-index-fund-direct-growth",
    "hdfc-corporate-debt-opportunities-fund-direct-growth"
]

def setup_driver():
    """Setup headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    import os
    # Use system Chrome on GitHub Actions, ChromeDriverManager locally
    if os.environ.get('GITHUB_ACTIONS'):
        # On GitHub Actions, use system Chrome
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        service = Service('/usr/bin/chromedriver')
    else:
        # Local development
        service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_value(text, patterns):
    """Extract value using regex patterns"""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def scrape_fund_complete(driver, fund_slug):
    """Scrape complete structured data from fund page"""
    url = f"https://groww.in/mutual-funds/{fund_slug}"
    
    try:
        print(f"  🌐 Loading {url}...")
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        # Get full page text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Extract structured data
        fund_data = {
            "page_url": url,
            "fund_name": driver.title.split('|')[0].strip(),
            "amc_name": "HDFC Mutual Fund",
            "category": extract_value(page_text, [r"(Equity|Debt|Hybrid)"]),
            "sub_category": extract_value(page_text, [r"(Mid Cap|Large Cap|Small Cap|Flexi Cap|ELSS|Balanced)"]),
            "plan_type": "Direct",
            "option": "Growth",
            "latest_nav": extract_value(page_text, [r"NAV:.*?₹([\d.]+)", r"₹([\d.]+)\s*NAV"]),
            "nav_date": extract_value(page_text, [r"NAV:\s*(\d{1,2}\s+\w+\s+\d{4})"]),
            "nav_change_pct": extract_value(page_text, [r"([+-][\d.]+%)\s*1D"]),
            "aum": extract_value(page_text, [r"Fund size\s*₹([\d,]+\.?\d*Cr)"]),
            "expense_ratio": extract_value(page_text, [r"Expense ratio[:\s]*([\d.]+%?)", r"expense ratio.*?([\d.]+)"]),
            "risk_level": extract_value(page_text, [r"(Very High Risk|High Risk|Moderately High Risk|Moderate Risk|Low Risk)"]),
            "rating": extract_value(page_text, [r"Rating\s*(\d)"]),
            "min_investment": {
                "lump_sum": extract_value(page_text, [r"Min\.?\s*investment\s*₹([\d,]+)"]),
                "sip": extract_value(page_text, [r"Min\.?\s*SIP amount\s*₹([\d,]+)"])
            },
            "exit_load": extract_value(page_text, [r"Exit load[:\s]*([^\\n]+)", r"exit load.*?([^\\n]{10,100})"]),
            "lock_in_period": extract_value(page_text, [r"Lock-in[:\s]*([^\\n]+)"]),
            "returns": {
                "1y": extract_value(page_text, [r"1Y.*?([\d.]+%)"]),
                "3y": extract_value(page_text, [r"3Y.*?([\d.]+%)"]),
                "5y": extract_value(page_text, [r"5Y.*?([\d.]+%)"])
            },
            "full_text": page_text[:10000],  # First 10k chars for context
            "scraped_at": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        
        print(f"  ✅ {fund_data['fund_name']}")
        print(f"     NAV: ₹{fund_data['latest_nav']}, Expense: {fund_data['expense_ratio']}")
        print(f"     Exit Load: {fund_data['exit_load'][:50] if fund_data['exit_load'] else 'Not found'}")
        print(f"     Min SIP: ₹{fund_data['min_investment']['sip']}")
        
        return fund_data
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def main():
    print("🚀 Starting complete data scraper...\n")
    
    driver = setup_driver()
    results = []
    
    try:
        for i, slug in enumerate(ALL_FUNDS, 1):
            print(f"[{i}/{len(ALL_FUNDS)}] Processing {slug}...")
            data = scrape_fund_complete(driver, slug)
            if data:
                results.append(data)
            time.sleep(2)
    
    finally:
        driver.quit()
    
    # Save results
    with open('data/complete_fund_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Scraped {len(results)} funds")
    print(f"💾 Saved to complete_fund_data.json")
    
    # Print summary
    print(f"\n📊 Summary:")
    for fund in results:
        print(f"  • {fund['fund_name']}")
        print(f"    NAV: ₹{fund['latest_nav']}, Expense: {fund['expense_ratio']}, Exit Load: {fund['exit_load'][:30] if fund['exit_load'] else 'N/A'}...")

if __name__ == "__main__":
    main()
