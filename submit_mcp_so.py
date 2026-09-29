import urllib.request
import urllib.parse
import json
import sys

# Submit to mcp.so free listing
url = "https://mcp.so/submit"

# mcp.so form data
form_data = {
    "repository_url": "https://github.com/emberfreellm/freellm-mcp",
    "name": "FreeLLM-MCP: free LLM availability and throughput MCP server"
}

# Encode form data
encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')

# Create request
req = urllib.request.Request(url, data=encoded_data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
req.add_header('User-Agent', 'Mozilla/5.0 (compatible; FreeLLM-MCP/1.0)')

# Enable handling redirects
handler = urllib.request.HTTPRedirectHandler()

# Build an opener that can handle redirects
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)

def main():
    try:
        # Submit and read response
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            print("Submission successful!")
            print("Response:", content[:500])
            
            # Check for success indicators
            if 'success' in content.lower() or 'thank' in content.lower() or 'submitted' in content.lower():
                print("✓ mcp.so submission accepted")
                sys.exit(0)
            else:
                print("⚠️  Response received but unclear if successful")
                sys.exit(1)
                
    except Exception as e:
        print(f"Submission failed: {e}")
        print("This is common for mcp.so form submission - they might use JavaScript or have additional requirements")
        sys.exit(1)

if __name__ == "__main__":
    main()