from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tournament import Tournament, TournamentDetail

#create driver/browser open page
driver = webdriver.Chrome()
driver.get('https://tss.warthunder.com/index.php?action=current_tournaments#')
driver.implicitly_wait(2.0)

def close_gdpr():
    print('closing GDPR')
    deny_button = driver.find_element(By.CSS_SELECTOR, "button[data-cookiefirst-action='reject']")
    driver.implicitly_wait(4.0)
    deny_button.click()
    driver.implicitly_wait(2.0)

def get_active_tournaments():
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

    detail_id = tournament_card.find_element(By.CSS_SELECTOR, 'a[card-name="buttonInfoTournament"]').get_attribute('href').split("=")[-1]

    data = {
        'title': tournament_card.find_element(By.CSS_SELECTOR, 'h3.header-name-tournament').text,
        'team_size': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='formatTeam']").text,
        'registrations': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='countTeam']").text,
        'battle_mode': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='gameMode']").text,
        'tournament_type': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='typeTournament']").text,
        'region': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='clusterTournament']").text,
        'tournament_date': tournament_card.find_element(By.CSS_SELECTOR, "p[card-name='dayTournament']").text,
        'detail_id': detail_id
    }

    return Tournament(**data)

def get_tournament_details(tournament):
    url = f'https://tss.warthunder.com/index.php?action=tournament&id={tournament.detail_id}'
    sub_driver = driver = webdriver.Chrome()
    sub_driver.get(url)
    
    data = {
        'id': tournament.detail_id,
        'prize_pool':  driver.find_element(By.CSS_SELECTOR, 'b[id-tss="prize_pool"]').text,
        #'maps': ,
        #'nations': , 
        #'vehicles': , 
    }

    sub_driver.quit()
    return data

def create_tournament_detail(data):
    return TournamentDetail(**data)

    

    

def main():
    #close gdpr 
    close_gdpr()
    

    #create list of active tournaments
    active_tournaments = get_active_tournaments()

    print('Creating Tournament Objects (printed from main)')
    for tournament in active_tournaments:
        tourn_obj = create_tournament_obj(tournament)
        tourn_detail_elements = get_tournament_details(tourn_obj)
        tourn_detail_obj = create_tournament_detail(tourn_detail_elements)

        print( tourn_obj.title, tourn_obj.date, "--", tourn_detail_obj.id, tourn_detail_obj.prize_pool )#, tourn_detail_obj.prize_pool )
    
    
    driver.quit()


    



main()
