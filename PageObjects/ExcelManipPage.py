from selenium.webdriver.common.by import By


class ExcelManipPage:

    def __init__(self, driver):
        self._driver = driver
        self.file_path = r'C:\Users\hkfir\Downloads\download.xlsx'

    # self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

    download = (By.CSS_SELECTOR, "button[id='downloadButton']")
    upload = (By.CSS_SELECTOR, "input[id = 'fileinput']")

    def download_file(self):
        self._driver.find_element(*ExcelManipPage.download).click()
        # TODO modify downloaded execl with updated value
        # purchase_products = PurchasePage(self._driver)
        # return purchase_products

    def upload_file(self):
        # for this operation to succeed you need to have ###type="file"#### attribute in your HTML page
        # since selenium cannot work with WIN pages directly
        self._driver.find_element(*ExcelManipPage.upload).send_keys(self.file_path)
