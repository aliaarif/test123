import csv
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from time import sleep


class GoogleMapScraper:
    def __init__(self):
        self.output_file_name = "data.csv"
        self.headless = False
        self.driver = None
        self.unique_check = []

    def config_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        driver.maximize_window()
        self.driver = driver

    def save_data(self, data):
        # header = ['business_name', 'business_slug', 'rating', 'reviews_count', 'address', 'category', 'phone', 'website']
        header = [
            'business_name',
            'business_slug',
            'business_category',
            'business_categoryslug',
            'business_phone',
            'business_email',
            'business_website',
            'business_address',
            'business_state',
            'business_city',
            'business_locality',
            'business_pin',
            'business_latitude',
            'business_longitude',
            'business_facebook',
            'business_social_instagram',
            'business_social_youtube',
            'business_timing_monday_start',
            'business_timing_monday_end',
            'business_timing_tuesday_start',
            'business_timing_tuesday_end',
            'business_timing_wednesday_start',
            'business_timing_wednesday_end',
            'business_timing_thrusday_start',
            'business_timing_thrusday_end',
            'business_timing_friday_start',
            'business_timing_friday_end',
            'business_timing_saturday_start',
            'business_timing_saturday_end',
            'business_timing_sunday_start',
            'business_timing_sunday_end',
            'business_description',
            'business_faqs_0_q',
            'business_faqs_1_q',
            'business_faqs_2_q',
            'business_faqs_0_a',
            'business_faqs_1_a',
            'business_faqs_2_a',
            'business_image_0_',
            'business_image_1',
            'business_image_2',
            'business_image_3',
            'business_image_4',
            'business_rating',
            'business_reviews_count',
            'business_category',
            'page_title',
            'page_content',
            'status',
            'created_by',
            'updated_by',
            'createdAt',
            'updatedAt'
        ]
        with open(self.output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if data[0] == 1:
                writer.writerow(header)
            writer.writerow(data)


    def parse_business_phone(self, business):
        try:
            contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[3].text.split("·")[-1].strip()
        except:
            contact = ""

        if "+1" not in contact:
            try:
                contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[4].text.split("·")[-1].strip()
            except:
                contact = ""

        return contact


    def parse_rating_and_review_count(self, business):
        try:
            reviews_block = business.find_element(By.CLASS_NAME, 'AJB7ye').text.split("(")
            business_rating = reviews_block[0].strip()
            business_reviews_count = reviews_block[1].split(")")[0].strip()
        except:
            business_rating = ""
            business_reviews_count = ""

        return business_rating, business_reviews_count


    def parse_business_address(self, business):
        try:
            address_block = business.find_elements(By.CLASS_NAME, "W4Efsd")[2].text.split("·")
            if len(address_block) >= 2:
                address = address_block[1].strip()
            elif len(address_block) == 1:
                address = ""
        except:
            address = ""

        return address
    
    def parse_business_address2(self, business):
        try:
            btn = business.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[15]/div[3]/button/div/div[2]/div[1]')
            business.click()
            sleep(2)
            address = self.driver.find_element(By.CLASS_NAME, 'Io6YTe').text
            print(address)
            # self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[3]/span/button').click()
        except:
            address = ""

        return address
    
    def parse_business_image_0(self, business):
        try:
            # business_image_0 = business.find_element(By.CLASS_NAME, 'fontHeadlineSmall')
            business_image_0 = ""
        except:
            business_image_0 = ""

        return business_image_0
    

    def parse_business_category(self, business):
        try:
            address_block = business.find_elements(By.CLASS_NAME, "W4Efsd")[2].text.split("·")
            if len(address_block) >= 2:
                business_category = address_block[0].strip()
            elif len(address_block) == 1:
                business_category = address_block[0]
        except:
            business_category = ""

        return business_category


    def get_business_info(self):
        time.sleep(2) # 2 second
        for business in self.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
            business_title = business.find_element(By.CLASS_NAME, 'fontHeadlineSmall')
            business_name = business_title.text
            business_slug = ''
            business_category = ''
            business_categoryslug = ''
            business_phone = self.parse_business_phone(business)
            business_email = ''
            try:
                business_website = business.find_element(By.CLASS_NAME, "lcr4fd").get_attribute("href")
            except NoSuchElementException:
                business_website = ""

            business_address = self.parse_business_address2(business)

            business_state = ''
            business_city = ''
            business_locality = ''
            business_pin = ''
            business_latitude = ''
            business_longitude = ''

            business_facebook = ''
            business_social_instagram = ''
            business_social_youtube = ''
            business_timing_monday_start = ''
            business_timing_monday_end = ''
            business_timing_tuesday_start = ''
            business_timing_tuesday_end = ''
            business_timing_wednesday_start = ''
            business_timing_wednesday_end = ''
            business_timing_thrusday_start = ''
            business_timing_thrusday_end = ''
            business_timing_friday_start = ''
            business_timing_friday_end = ''
            business_timing_saturday_start = ''
            business_timing_saturday_end = ''
            business_timing_sunday_start = ''
            business_timing_sunday_end = ''
            business_description = ''
            business_faqs_0_q = ''
            business_faqs_1_q = ''
            business_faqs_2_q = ''
            business_faqs_0_a = ''
            business_faqs_1_a = ''
            business_faqs_2_a = ''
            business_image_0 = self.parse_business_image_0(business),
            business_image_1 = self.parse_business_image_0(business),
            business_image_2 = self.parse_business_image_0(business),
            business_image_3 = self.parse_business_image_0(business),
            business_image_4 = self.parse_business_image_0(business),
            business_rating = '',
            business_reviews_count = '',
            business_category = '',
            page_title = ''
            page_content = ''
            status = ''
            created_by = ''
            updated_by = ''
            createdAt = ''
            updatedAt = ''


            business_rating, business_reviews_count = self.parse_rating_and_review_count(business)
            business_category = self.parse_business_category(business)



            unique_id = "".join([business_phone, business_website, business_rating, business_reviews_count, business_category])
            # unique_id = "".join([name])
            if unique_id not in self.unique_check:
                data = [business_name,business_slug,business_category,business_categoryslug,business_phone,business_email,business_website,business_address,business_state,business_city,business_locality,business_pin,business_latitude,business_longitude,business_facebook,
                    business_social_instagram,
                    business_social_youtube,
                    business_timing_monday_start,
                    business_timing_monday_end,
                    business_timing_tuesday_start,
                    business_timing_tuesday_end,
                    business_timing_wednesday_start,
                    business_timing_wednesday_end,
                    business_timing_thrusday_start,
                    business_timing_thrusday_end,
                    business_timing_friday_start,
                    business_timing_friday_end,
                    business_timing_saturday_start,
                    business_timing_saturday_end,
                    business_timing_sunday_start,
                    business_timing_sunday_end,
                    business_description,
                    business_faqs_0_q,
                    business_faqs_1_q,
                    business_faqs_2_q,
                    business_faqs_0_a,
                    business_faqs_1_a,
                    business_faqs_2_a,
                    business_image_0,
                    business_image_1,
                    page_title,
                    page_content,
                    status,
                    created_by,
                    updated_by,
                    createdAt,
                    updatedAt
                    ]
                self.save_data(data)
                self.unique_check.append(unique_id)
            else:
                pass    
                



    def load_companies(self, url):
        print("Getting business info", url)
        self.driver.get(url)
        time.sleep(2)
        panel_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
        # panel_xpath = '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]'
        scrollable_div = self.driver.find_element(By.XPATH, panel_xpath)
        # scrolling
        flag = True
        i = 0
        while flag:
            print(f"Scrolling to page {i + 2}")
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)

            if "You've reached the end of the list." in self.driver.page_source:
                flag = False

            self.get_business_info()
            i += 1


urls = [
    "https://www.google.com/maps/search/hotels+in+gurgaon",
]

business_scraper = GoogleMapScraper()
business_scraper.config_driver()
for url in urls:
    business_scraper.load_companies(url)