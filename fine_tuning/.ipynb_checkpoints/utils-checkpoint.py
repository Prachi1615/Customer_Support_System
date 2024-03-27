def keyword_search(query, 
                   client,
                   results_lang='en', 
                   properties = ["title", "content"],
                   num_results=3):

    where_filter = {
    "path": ["lang"],
    "operator": "Equal",
    "valueString": results_lang
    }

    response = (
        client.query.get("Article", properties)
        .with_bm25(
          query=query
        )
        .with_limit(3)
        .do()
        )
    result = response['data']['Get']['Article']
    return result


def dense_retrieval(query, 
                    client,
                    results_lang='en', 
                    properties = ["title", "content"],
                    num_results=5):

    nearText = {"concepts": [query]}
    
    # To filter by language
    where_filter = {
    "path": ["lang"],
    "operator": "Equal",
    "valueString": results_lang
    }
    response = (
        client.query
        .get("Article", properties)
        .with_near_text(nearText)
        .with_limit(num_results)
        .do()
    )

    result = response['data']['Get']['Article']

    return result


def print_result(result):
    """ Print results with colorful formatting """
    for i,item in enumerate(result):
        print(f'item {i}')
        for key in item.keys():
            print(f"{key}:{item.get(key)}")
            print()
        print()