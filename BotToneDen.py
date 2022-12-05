import pyperclip # The name you have the file
from selenium import webdriver
import time
import pandas as pd

class Bot(webdriver.Firefox):

    """
    Bot design to make actions in the platform of ToneDen,

    actions available in the moment are:
        - sign in
        - create musics campaings form a DataFrame (A spotify link)
        - eliminate all campaings

    Argumments
    -----------

    email : str, the email asociated with the account
    password : str, password of the account


    Opcional Args
    ---------------

    teardown: bool, this argument is for the case of using the 'with' statement
    when using the with statement and the arg teardown is True, after finishing
    the assigned task the browser will close, per example;

        with Bot('something@gmail.com', 'secret' teardown = True) as bot:

            bot.do_something_cool()

        after the bot has done something cool, and after the with statement has finished
        the browser will close.



    With this bot it is expected to have installed Firefox and the gecko driver
    compatible with the version of said browser, doesn't necessarily mean you
    need to install firefox, it can be easily changed to Chrome / Opera / Edge,
    but you need to have the driver installed in your computer of said browser
    you can search it up and throw a pip install in the terminal

    """

    def __init__(self, email: str, password: str, teardown=False):
        self.teardown = teardown
        self.email = email
        self.password = password
        super(Bot, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def go_to(self, url = 'https://www.toneden.io/login'):
        self.get(url)

    def login(self):
        """
        Logs in the ToneDen account with the information provided
        """
        self.implicitly_wait(2000)

        email = self.find_element_by_xpath(
        '/html/body/div[1]/span/div[1]/div/div/div/span/div/div/div/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/input'
        )
        password = self.find_element_by_xpath(
        '/html/body/div[1]/span/div[1]/div/div/div/span/div/div/div/div[2]/div[4]/div/div[1]/div[2]/div/div[2]/input'
        )

        email.click()
        email.send_keys(self.email)

        password.click()
        password.send_keys(self.password)

        button = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/span/div/div/div/div[2]/div[4]/div/div[3]/a'
        )
        button.click()

    def create_music_campaign(self):
        """
        Creates a music campaigns
        """

        button_camp = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/header/nav/div/div[2]/table/tbody/tr/td[1]/a'
        )
        button_camp.click()

        smart_link = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div'
        )
        smart_link.click()

        select_music = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/div/div/div/div[2]/div/div[1]'
        )
        select_music.click()

        existing_release = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/div/div/div/div[2]/div/div[1]'
        )
        existing_release.click()

    def complete_forms(self, url):
        track_url = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/textarea'
        )
        track_url.click()
        track_url.send_keys(url)

        button_create_link = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[2]/div/div[2]/div[2]/button'
        )
        button_create_link.click()

        # pantalla con los servicios musicales
        button_continue = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[3]/div[2]/button'
        )
        button_continue.click()

        # personalize landing page
        button_continue2 = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[2]/div[1]/div/div[2]/button'
        )
        button_continue2.click()

        # customize preview
        button_continue3 = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[2]/div[1]/div[2]/div[2]/button'
        )
        button_continue3.click()


        # edit metadata
        button_continue4 = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[2]/div[1]/div[2]/div[2]/button'
        )
        button_continue4.click()

        # modify link URL
        button_continue5 = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[3]/div[2]/button'
        )
        button_continue5.click()

        # Tracking Settings
        button_continue6 = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[4]/div[2]/button'
        )
        button_continue6.click()

        # create link
        create_link_final = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/section/section/div/div/div/div/div[3]/div[2]/a'
        )
        create_link_final.click()

        # copy final link
        link_final = self.find_element_by_xpath(
            '/html/body/div[1]/span/div[1]/div/div/div/span/span/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/a[3]'
        )
        link_final.click()

        # copies the clibboard
        link = pyperclip.paste()

        return link

    def create_links(self, df):

        """
        returns the initial df with the aditional column, the link from the
        campaign

        This function goes to the page and log's in

        Arguments
        ----------
        df : dataframe with the links of the tracks the dataframe has to have
        the column of links named 'link'

        """

        self.go_to()
        self.login()

        links_finales = []
        for url in df['link']:
            self.go_to(url = 'https://www.toneden.io/calendar')

            if url == ':(':
                links_finales.append(':(')
            else:
                self.create_music_campaign()
                links_finales.append(self.complete_forms(url))
                time.sleep(2)

        tmp = pd.DataFrame(links_finales, columns = ['multi_link'])
        tmp2 = df.copy()

        df_final = pd.concat((tmp2,tmp), axis=1)
        df_final.to_csv('data/final_songs.csv')

        return df_final.copy()

    def borrar_links(self):
        """
        Eliminates all the campigns of your account
        """

        self.implicitly_wait(200)
        self.go_to()

        time.sleep(1)
        self.login()
        time.sleep(2)

        self.check_all_campigns_to_eliminate()

    def check_all_campigns_to_eliminate(self):
        """
        Eliminates all the campaings checks the /links page until there's no campign
        checks two times the page to make sure that there's no residue
        """

        check_bool = False
        check_num = 0

        self.go_to(url = 'https://www.toneden.io/links')

        time.sleep(2)
        lst_links = self.get_links_to_elim()

        self.actions_elim_campaigns(lst_links)

        while check_bool != True:
            self.go_to(url = 'https://www.toneden.io/links')
            time.sleep(4)
            lst_links = self.get_links_to_elim()
            if self.actions_elim_campaigns(lst_links) == 'time_to_check':
                check_num += 1
                if check_num == 2:
                    check_bool = True

        print("\n\nThere's no campaings left!!\n")

    def get_links_to_elim(self):

        """
        Gets the links to the insights page of the campaigns by webscrapping
        """

        from bs4 import BeautifulSoup

        source = self.page_source
        source = BeautifulSoup(source, 'html.parser')

        lst_links = []

        for i in source.find_all('a'):

            tmp = i.get('href')

            if tmp != None:
                if '/links/' in tmp:

                    tmp = 'https://www.toneden.io' + tmp
                    lst_links.append(tmp)

        return lst_links

    def actions_elim_campaigns(self, lst_links):

        """
        Eliminates the campigns
        """

        if len(lst_links) == 0:
            return 'time_to_check'

        else:
            for link in lst_links:

                self.go_to(url = link)

                delete_button = self.find_element_by_xpath(
                    '/html/body/div[1]/span/div[1]/div/div/div/span/span/div/div[2]/div/div/div[1]/div/div[2]/div/div[6]/a'
                )
                delete_button.click()

                confirm_deletion = self.find_element_by_css_selector(
                    'button.eds-btn:nth-child(2)'
                )
                confirm_deletion.click()
