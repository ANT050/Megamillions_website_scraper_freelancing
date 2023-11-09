import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


def get_html_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    html_page = driver.page_source

    driver.quit()

    return html_page


def parse_html(html_page):
    soup = BeautifulSoup(html_page, 'lxml')

    draw_dates_text = [element.get_text() for element in soup.find_all(class_='drawItemDate')]
    megaplayer_text = [element.get_text() for element in soup.find_all(class_='megaplier pastNumMP')]
    winning_numbers_elements = soup.find_all('li',
                                             class_=['ball pastNum1',
                                                     'ball pastNum2',
                                                     'ball pastNum3',
                                                     'ball pastNum4',
                                                     'ball pastNum5',
                                                     'ball yellowBall pastNumMB'])

    return draw_dates_text, megaplayer_text, winning_numbers_elements


def process_data(draw_dates_text, megaplayer_text, winning_numbers_elements):
    results = []

    for i in range(0, len(draw_dates_text)):
        draw_date = draw_dates_text[i]
        megaplayer = megaplayer_text[i]
        winning_numbers = " ".join(result.get_text() for result in winning_numbers_elements[i * 6:i * 6 + 6])
        group_winning_numbers = winning_numbers[:-2] + " + " + winning_numbers[-2:]
        result_dict = {
            'draw_dates': draw_date,
            'winning_numbers': group_winning_numbers,
            'megaplayer': megaplayer
        }
        results.append(result_dict)

    return results


def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.columns = ['draw_dates', 'winning_numbers', 'megaplayer']
    df.to_excel(output_file, index=False, engine='openpyxl')


def main():
    url = 'https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx#page12'
    html_page = get_html_page(url)
    draw_dates_text, megaplayer_text, winning_numbers_elements = parse_html(html_page)
    results = process_data(draw_dates_text, megaplayer_text, winning_numbers_elements)
    save_to_excel(results, 'previous_drawings.xlsx')


if __name__ == '__main__':
    main()
