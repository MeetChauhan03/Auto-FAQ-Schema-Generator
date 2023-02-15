import requests
from bs4 import BeautifulSoup
import json

# Define the URL
url = input("Enter website FAQ page URL: ")
Question=input("Enter question class name:")
Answer=input("Enter Answer class name:")
# Make a request to the website
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Extract the questions and answers
main_entity = {}
for item in soup.find_all("div", class_=Question):
    question = item.text.strip()
    answer = item.find_next_sibling("div", class_=Answer).text.strip()
    main_entity.append({
        "@type": "Question",
        "name": question,
        "acceptedAnswer": {
            "@type": "Answer",
            "text": answer
        }
    })

# Write the faq_format to a file
faq_format = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": main_entity
}

with open("faq.html", "w") as f:
    f.write('<script type="application/ld+json">\n')
    json.dump(faq_format, f, indent=2)
    f.write('\n</script>')