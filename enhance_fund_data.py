#!/usr/bin/env python3
"""
Improved scraper - extracts NAV, returns, exit load, managers, holdings
Uses complete_fund_data.json and enhances it with better extraction
"""

import json
import re

def extract_nav(text):
    """Extract NAV value"""
    match = re.search(r'NAV:.*?₹([\d,]+\.?\d*)', text)
    return f"₹{match.group(1)}" if match else None

def extract_returns(text):
    """Extract 1Y, 3Y, 5Y returns"""
    returns_1y = re.search(r'Fund returns\s+([\d.]+%)', text)
    # Look for 3Y and 5Y in the returns table
    returns_section = re.search(r'3Y\s+5Y.*?Fund returns\s+([\d.]+%)\s+([\d.]+%)', text, re.DOTALL)
    
    if returns_section:
        return {
            "1y": returns_1y.group(1) if returns_1y else None,
            "3y": returns_section.group(1),
            "5y": returns_section.group(2)
        }
    return {"1y": None, "3y": None, "5y": None}

def extract_exit_load_full(text):
    """Extract complete exit load text"""
    match = re.search(r'Exit load\s+(.*?)(?:Stamp duty|Tax implication)', text, re.DOTALL)
    if match:
        return match.group(1).strip()[:200]
    return "Nil"

def extract_fund_managers(text):
    """Extract fund manager names"""
    # Pattern: Name + Month Year - Present
    matches = re.findall(r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s+-\s+Present', text)
    return list(set(matches))[:3]

def main():
    print("🔧 Enhancing fund data with improved extraction...\n")
    
    # Load existing data
    with open('complete_fund_data.json', 'r') as f:
        funds = json.load(f)
    
    enhanced_funds = []
    
    for i, fund in enumerate(funds, 1):
        print(f"[{i}/{len(funds)}] Enhancing {fund['fund_name'][:50]}...")
        
        text = fund['full_text']
        
        # Extract improved fields
        nav = extract_nav(text)
        returns = extract_returns(text)
        exit_load = extract_exit_load_full(text)
        managers = extract_fund_managers(text)
        
        # Create enhanced fund
        enhanced = {
            **fund,  # Keep all existing fields
            "latest_nav": nav or fund.get('latest_nav'),
            "returns": returns if any(returns.values()) else fund.get('returns', {}),
            "exit_load": exit_load if exit_load != "a" else fund.get('exit_load'),
            "fund_managers": managers if managers else []
        }
        
        enhanced_funds.append(enhanced)
        
        print(f"  ✅ NAV: {nav}, 3Y: {returns.get('3y', 'N/A')}, Managers: {len(managers)}")
    
    # Save
    with open('enhanced_fund_data.json', 'w') as f:
        json.dump(enhanced_funds, f, indent=2)
    
    print(f"\n✅ Enhanced {len(enhanced_funds)} funds")
    print(f"💾 Saved to enhanced_fund_data.json")

if __name__ == "__main__":
    main()
