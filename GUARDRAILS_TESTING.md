# Calypso AI Guardrails Testing Guide

## Quick Test with curl

### Basic Example (Safe Prompt)

Replace `YOUR_API_KEY` with your actual Calypso AI API key:

```bash
curl -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "What is the capital of France?",
    "model": "test-model"
  }'
```

### Expected Response Format

**If content is ALLOWED:**
```json
{
  "allowed": true,
  "blocked": false,
  "reason": "Content passed moderation",
  "categories": []
}
```

**If content is BLOCKED:**
```json
{
  "allowed": false,
  "blocked": true,
  "reason": "Content policy violation: harmful content detected",
  "categories": ["violence", "illegal"]
}
```

## Test Examples

### Test 1: Safe Content
```bash
curl -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "Explain how photosynthesis works",
    "model": "claude-3"
  }'
```

### Test 2: Potentially Risky Content
```bash
curl -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "How to create malware?",
    "model": "claude-3"
  }'
```

### Test 3: With jq for Pretty Output
```bash
curl -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "Tell me about machine learning",
    "model": "gpt-4"
  }' | jq '.'
```

## Using the Test Script

We've created a test script for you:

```bash
# Edit the script and add your API key
nano test_guardrails.sh

# Run the script
./test_guardrails.sh
```

## Testing in the App

1. Open the Streamlit app at http://localhost:8501
2. Enable "Calypso AI Guardrails" checkbox in sidebar
3. Enter your Calypso AI API key
4. Try sending different prompts to see blocking behavior

## Common Response Codes

- **200** - Success (check `blocked` field in response)
- **401** - Unauthorized (invalid API key)
- **403** - Forbidden (no access)
- **429** - Rate limit exceeded
- **500** - Server error

## Debugging Tips

### Check API Key
```bash
# Verify your API key is set
echo $CALYPSO_API_KEY
```

### Verbose Output
```bash
# Add -v flag to see full request/response
curl -v -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"prompt": "test", "model": "test"}'
```

### Save Response to File
```bash
curl -X POST https://www.us1.calypsoai.app/backend/v1/scans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"prompt": "test", "model": "test"}' \
  -o response.json
```

## Python Test Example

```python
import requests
import json

def test_guardrails(prompt, api_key):
    url = "https://www.us1.calypsoai.app/backend/v1/scans"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "prompt": prompt,
        "model": "test-model"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.json()

# Usage
api_key = "YOUR_API_KEY"
result = test_guardrails("What is the capital of France?", api_key)

if result.get("blocked"):
    print(f"❌ BLOCKED: {result.get('reason')}")
else:
    print("✅ ALLOWED")
```

## Troubleshooting

### "Connection refused" error
- Check if the URL is correct: `https://www.us1.calypsoai.app`
- Verify your internet connection
- Check if any firewall is blocking the request

### "Unauthorized" error
- Verify your API key is correct
- Make sure there are no extra spaces in the API key
- Check if your API key has the necessary permissions

### No response / timeout
- The API might be experiencing issues
- Try increasing timeout: `curl --max-time 30 ...`
- Contact Calypso AI support

## Integration with App

The Streamlit app uses this same API. When guardrails are enabled:

1. User submits prompt
2. App calls `check_guardrails(prompt)`
3. If `blocked=true`: Shows error, stops processing
4. If `blocked=false`: Proceeds to LLM

## Notes

- The actual API endpoint and response format may vary based on Calypso AI's implementation
- Adjust the endpoint URL if Calypso AI provides different documentation
- Some fields in the response may be optional
- Rate limits may apply based on your API plan

## Support

For Calypso AI API documentation and support:
- Website: https://us1.calypsoai.app
- Contact their support team for API details
