#!/usr/bin/env python3
"""
Upload enhanced fund data to Pinecone - ONE VECTOR AT A TIME
"""

import json
import requests
import time

GEMINI_API_KEY = "AIzaSyDIXRjgctybCWCCNRINIupbSZSD7ILs7nQ"
PINECONE_API_KEY = "pcsk_6zqhGY_8iWUvrG6RwhWYHC2aW6i7D3EqtUdCiKvxZcaqY925oFtoMiXbuE4GMYShTeVEEf"
PINECONE_HOST = "fees-explainer-2znm61p.svc.aped-4627-b74a.pinecone.io"

def get_embedding(text):
    """Get embedding from Gemini"""
    url = f"https://generativelanguage.googleapis.com/v1/models/text-embedding-004:embedContent?key={GEMINI_API_KEY}"
    payload = {"content": {"parts": [{"text": text}]}}
    response = requests.post(url, json=payload)
    return response.json()['embedding']['values']

def create_document(fund):
    """Create comprehensive document"""
    exit_load_text = fund.get('exit_load', 'Nil')
    if exit_load_text == "a":
        exit_load_text = "Exit load of 1% if redeemed within 1 year"
    
    doc = f"""
Fund: {fund['fund_name']}
Category: {fund['category']} - {fund['sub_category']}
Risk: {fund['risk_level']}
Rating: {fund['rating']}

FEES:
- Expense Ratio: {fund['expense_ratio']}
- Exit Load: {exit_load_text}
- Min SIP: {fund['min_investment']['sip']}
- Min Lumpsum: {fund['min_investment']['lump_sum'] or 'Same as SIP'}

TAXATION:
- STCG (< 1 year): 20%
- LTCG (> 1 year): 12.5% (above ₹1.25 lakh)

RETURNS:
- 1Y: {fund['returns'].get('1y', 'N/A')}
- 3Y: {fund['returns'].get('3y', 'N/A')}
- 5Y: {fund['returns'].get('5y', 'N/A')}

FUND DETAILS:
- AUM: {fund['aum']}
- NAV: {fund['latest_nav'] or 'Check Groww.in'}
- NAV Date: {fund['nav_date']}
- Managers: {', '.join(fund.get('fund_managers', []))}

Source: {fund['page_url']}
Last Updated: {fund['scraped_at']}
"""
    return doc

def upload_one_vector(fund, index):
    """Upload single vector to Pinecone"""
    try:
        # Create document
        doc = create_document(fund)
        
        # Get embedding
        embedding = get_embedding(doc)
        
        # Create vector with comprehensive metadata
        fund_id = fund['fund_name'].replace(' ', '_').replace('-', '_').replace('&', 'and')[:50]
        
        # Prepare fund managers as comma-separated string
        managers = ', '.join(fund.get('fund_managers', [])) if fund.get('fund_managers') else 'N/A'
        
        vector = {
            'id': fund_id,
            'values': embedding,
            'metadata': {
                'fund_name': str(fund['fund_name'])[:100],
                'category': str(fund.get('category') or 'N/A'),
                'sub_category': str(fund.get('sub_category') or 'N/A'),
                'plan_type': str(fund.get('plan_type') or 'Direct'),
                'aum': str(fund.get('aum') or 'N/A'),
                'expense_ratio': str(fund.get('expense_ratio') or 'N/A'),
                'risk_level': str(fund.get('risk_level') or 'N/A'),
                'rating': str(fund.get('rating') or 'N/A'),
                'min_sip': str(fund['min_investment'].get('sip') or 'N/A'),
                'exit_load': str(fund.get('exit_load') or 'N/A')[:200],
                'returns_1y': str(fund['returns'].get('1y', 'N/A')),
                'returns_3y': str(fund['returns'].get('3y', 'N/A')),
                'returns_5y': str(fund['returns'].get('5y', 'N/A')),
                'fund_managers': managers[:200],
                'source_url': str(fund['page_url']),
                'text': doc[:1000]
            }
        }
        
        # Upload
        url = f"https://{PINECONE_HOST}/vectors/upsert"
        headers = {'Api-Key': PINECONE_API_KEY, 'Content-Type': 'application/json'}
        payload = {'vectors': [vector], 'namespace': 'fund-documents'}
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Uploaded ({result.get('upsertedCount', 0)} vectors)")
            return True
        else:
            print(f"  ❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("🚀 Uploading enhanced fund data to Pinecone (one at a time)...\n")
    
    # Delete old data
    print("🗑️  Deleting old vectors...")
    url = f"https://{PINECONE_HOST}/vectors/delete"
    headers = {'Api-Key': PINECONE_API_KEY, 'Content-Type': 'application/json'}
    payload = {'deleteAll': True, 'namespace': 'fund-documents'}
    requests.post(url, headers=headers, json=payload)
    print("✅ Deleted\n")
    
    # Load data
    with open('data/enhanced_fund_data.json', 'r') as f:
        funds = json.load(f)
    
    print(f"📂 Loaded {len(funds)} funds\n")
    
    # Upload one by one
    success_count = 0
    for i, fund in enumerate(funds, 1):
        print(f"[{i}/{len(funds)}] {fund['fund_name'][:50]}...")
        if upload_one_vector(fund, i):
            success_count += 1
        time.sleep(1)  # Rate limiting
    
    print(f"\n✅ Successfully uploaded {success_count}/{len(funds)} funds")
    
    # Verify
    time.sleep(3)
    stats_url = f"https://{PINECONE_HOST}/describe_index_stats"
    response = requests.post(stats_url, headers={'Api-Key': PINECONE_API_KEY})
    stats = response.json()
    print(f"📊 Pinecone now has {stats.get('totalVectorCount', 0)} vectors")
    print(f"\n🎉 Complete! Ready to test AI Agent.")

if __name__ == "__main__":
    main()
