from selenium.webdriver.support.ui import Select
from model.project import Project

class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[value='Login']").click()


    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()
        wd.find_element_by_name("username")


    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)


    def create_project(self, project):
        wd = self.app.wd
        self.app.open_edit_page()
        self.fill_project_form(project)
        self.project_cache = None

    def delete_project(self, project):
        wd = self.app.wd
        self.app.open_project_list()
        wd.find_element_by_link_text(project.project_name).click()
        wd.find_element_by_css_selector("form > input.button").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_css_selector("input.button").click()
        self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.project_name)
        Select(wd.find_element_by_name('status')).select_by_visible_text(project.status)
        if project.is_inherited is not True:
            pass
        wd.find_element_by_name('inherit_global').click()
        Select(wd.find_element_by_name('view_state')).select_by_visible_text(project.view_status)
        wd.find_element_by_name("description").send_keys(project.desc)
        wd.find_element_by_css_selector("input[value='Add Project']").submit()

    project_cache = None
    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.app.open_project_list()
            self.project_cache = []
            for element in wd.find_elements_by_css_selector("table.width100 tr[class^='row']")[1:]:
                cells = element.find_elements_by_tag_name("td")
                project_name = cells[0].text
                status = cells[1].text
                is_inherited = cells[2].text
                view_status = cells[3].text
                desc = cells[4].text
                id = element.find_element_by_css_selector('a').get_attribute("href").split('=')[-1]
                self.project_cache.append(Project(id=id, project_name=project_name, status=status, is_inherited=is_inherited, view_status=view_status, desc=desc))
        return list(self.project_cache)


