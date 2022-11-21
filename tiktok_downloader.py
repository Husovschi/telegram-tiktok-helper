import requests

from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

DELAY = 3
SOURCE_URL = 'https://snaptik.app/en'


class TiktokDownloader:

    def __init__(self) -> None:
        self.op = Options()
        self.set_arguments()

        self.driver = webdriver.Firefox(options=self.op)
        self.wait = WebDriverWait(
            self.driver,
            DELAY,
            poll_frequency=1,
            ignored_exceptions=[
                ElementNotVisibleException,
                ElementNotSelectableException
            ]
        )

    def set_arguments(self) -> None:
        self.op.add_argument("--headless")
        self.op.add_argument("--disable-gpu")

    def download_video(self, url) -> None:
        self.driver.get(SOURCE_URL)
        text_url = self.wait.until(EC.presence_of_element_located((By.ID, "url")))
        text_url.send_keys(url)

        text_submit = self.driver.find_element(By.CLASS_NAME, 'flex-center')
        text_submit.click()

        no_watermark_button = self.wait.until(lambda x: x.find_element(By.CLASS_NAME, "mb-2"))

        video_url = no_watermark_button.get_attribute("href")

        r = requests.get(video_url)

        with open('out.mp4', "wb") as f:
            f.write(r.content)
        f.close()
        self.driver.close()
