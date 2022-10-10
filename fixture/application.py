from selenium import webdriver
from fixture.session import SessionHelper



class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "opera":
            self.wd = webdriver.Opera()
        else:
            raise ValueError("Unrecognised browser argument: %s" % browser)
        self.wd.implicitly_wait(3)
        self.session = SessionHelper(self)
        self.base_url = base_url


    def open_home_page(self):
        wd = self.wd
        if not (wd.current_url.endswith('/addressbook/') and len(wd.find_elements_by_link_text("Last name")) > 0):
            wd.get(self.base_url)

    def open_edit_page(self):
        wd = self.wd
        if not (wd.current_url.endswith('/manage_proj_create_page.php/') and len(wd.find_elements_by_css_selector("input[value='Add Project']")) > 0):
            wd.get('http://172.17.41.29/mantisbt-1.2.20/manage_proj_create_page.php')

    def open_project_list(self):
        wd = self.wd
        if not (wd.current_url.endswith('/manage_proj_page.php') and len(wd.find_elements_by_css_selector("input[value='Add Category']")) > 0):
            wd.get('http://172.17.41.29/mantisbt-1.2.20/manage_proj_page.php')


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False


    def destroy(self):
        self.wd.quit()
