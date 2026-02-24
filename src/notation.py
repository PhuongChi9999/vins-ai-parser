import re


def find_score(soup, evaluator):
    critic_blocks = soup.find_all("div", attrs={"data-rbf": "wine-critic-slide"})
    if not critic_blocks:
        return None

    for critic_block in critic_blocks:
        spans = critic_block.find_all("span")
        if len(spans) < 2:
            continue

        name = spans[0].text.strip()
        if evaluator.lower() in name.lower():
            score_with_grade = spans[1].text.strip()

            # Delete + symbol and grating scale
            score_row = re.split(r"/|\+", score_with_grade)
            main_score = score_row[0]

            # If we have a range score, then we take the average
            if "-" in main_score:
                print("main_score=" + main_score)
                prx = main_score.split("-", 2)
                start=0
                if(prx[0] != ''):
                    start=float(prx[0])
                
                end=start
                if(prx[1] != ''):
                    start=float(prx[1])
                    
                #start, end = map(float, main_score.split("-"))
                return (start + end) / 2

            # Otherwise, we convert the score to float
            try:
                return float(main_score)
            except ValueError:
                return None

    return None

def parker(soup):
    return find_score(soup, "Parker")

def robert(soup):
    return find_score(soup, "Robert")


def robinson(soup):
    return find_score(soup, "Robinson")


def suckling(soup):
    return find_score(soup, "Suckling")
