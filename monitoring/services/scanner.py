from monitoring.models import Keyword, ContentItem, Flag
from .matcher import calculate_score
import requests
from django.utils.timezone import now


def run_scan():
    contents = fetch_external_content()
    keywords = Keyword.objects.all()

    for keyword in keywords:
        for content in contents:
            score = calculate_score(keyword.name, content)

            if score > 0:

                existing_flag = Flag.objects.filter(
                    keyword=keyword,
                    content_item=content
                ).order_by('-id').first()

                if existing_flag:
                    if existing_flag.status == 'irrelevant':
                        if existing_flag.reviewed_at and content.last_updated > existing_flag.reviewed_at:
                            pass
                        else:
                            continue
                    else:
                        continue

                Flag.objects.create(
                    keyword=keyword,
                    content_item=content,
                    score=score,
                    status='pending'
                )



def fetch_external_content():
    print("FETCH STARTED")

    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        return []

    data = response.json()[:10]

    print("DATA LENGTH:", len(data))

    created_items = []

    for item in data:
        print("PROCESSING:", item['title'])

        content, created = ContentItem.objects.get_or_create(
            title=item['title'],
            defaults={
                'body': item['body'],
                'source': 'api',
                'last_updated': now()
            }
        )

        print("CREATED:", created)

        created_items.append(content)

    print("TOTAL CREATED:", len(created_items))

    return created_items