from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from tournament import Tournament




#create driver/browser open page
def setup_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument('start-maximized')  #
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")

    # Set path to chromedriver as needed
    service = Service(executable_path='chrome_driver/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def close_gdpr(driver):
    print('closing GDPR')
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "button[data-cookiefirst-action='reject']")))
        deny_button = driver.find_element(By.CSS_SELECTOR, "button[data-cookiefirst-action='reject']")
        deny_button.click()
    except Exception as e:
        print(f'Failed to close GDPR: {str(e)}')

def get_active_tournaments(driver):
    past_card = driver.find_elements(By.CSS_SELECTOR, ".row.container_info_tournament.past")
    active_tournaments = []
    more_btn = driver.find_element(By.ID, 'linkLoadTournaments')
    #initial page load card gather

    #check for inactive cards to signify end of active cards list
    while not past_card:
        print('clicking more')
        more_btn.click()
        past_card = driver.find_elements(By.CSS_SELECTOR, ".row.container_info_tournament.past")
    print('found past card')
    
    #gather active_cards
    active_cards = driver.find_elements(By.CSS_SELECTOR, '.row.container_info_tournament.open')
    for card in active_cards:
        active_tournaments.append(card)
    print(f'total_tournaments: {len(active_tournaments)}')

    #figure out a proper return
    return (active_tournaments)

def create_tournament_obj(tournament_card):
    data = {
        'title': tournament_card.find_element(By.CSS_SELECTOR, 'h3.header-name-tournament').text,
        'team_size': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='formatTeam']").text,
        'registrations': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='countTeam']").text,
        'battle_mode': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='gameMode']").text,
        'tournament_type': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='typeTournament']").text,
        'region': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='clusterTournament']").text,
        'tournament_date': tournament_card.find_element(By.CSS_SELECTOR, "p[card-name='dayTournament']").text
    }

    return Tournament(**data )
    

def main():
    driver = setup_driver()
    driver.get("https://tss.warthunder.com/index.php?action=current_tournaments#")
    
    #close gdpr 
    close_gdpr(driver)


    active_tournaments = get_active_tournaments(driver)


    print('Creating Tournament Objects (printed from main)')
    for tournament in active_tournaments:
        tourn_obj = create_tournament_obj(tournament)
        print(tourn_obj.title, tourn_obj.date)
    driver.quit()



if __name__ ==  '__main__':
    main()
