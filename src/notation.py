import json
import re


def find_score(soup, evaluator):
    script = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script or not script.string:
        return None
    
    data = json.loads(script.string)

    # Table is built by Next.js. We have no access to table data. So we need to parse it manually.
    try:
       critics= data["props"]["pageProps"]["ratings"]
       for critic in critics:
            if evaluator.lower() in critic["critic"].lower():
                score_with_grade = critic["note"].strip()

                # Delete + symbol and grating scale
                score_row = re.split(r"/|\+", score_with_grade)
                main_score = score_row[0]

                # If we have a range score, then we take the average
                if "-" in main_score:
                    parts = main_score.split("-", 1)
                    start = float(parts[0])
                    try:
                        end = float(parts[1])
                    except (ValueError, IndexError):
                        return start
                    return (start + end) / 2

                # Otherwise, we convert the score to float
                try:
                    return float(main_score)
                except ValueError:
                    return None
    except KeyError:
        print("Score doesn't exist")

    return None

def parker(soup):
    return find_score(soup, "Parker")


def robinson(soup):
    return find_score(soup, "Robinson")


def suckling(soup):
    return find_score(soup, "Suckling")