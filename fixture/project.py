from model.project import Project
from selenium.webdriver.support.select import Select
import string
import random
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def random_string(self, prefix, maxlen):
        symbols = string.ascii_letters + string.digits + " " * 10
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    def create(self, project):
        wd = self.app.wd
        self.open_projects_management_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.project_cache = None

    def create_simple_project(self):
        project = Project(name=self.random_string("name", 10), status="development", view_status="private",
                          description="description")
        self.create(project)

    def open_projects_management_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/mantisbt-1.2.20/manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("status").click()
        Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
        wd.find_element_by_name("view_state").click()
        Select(wd.find_element_by_name("view_state")).select_by_visible_text(project.view_status)
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)

    def get_projects_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_management_page()
            self.project_cache = []

            elements = wd.find_elements_by_xpath("/html/body/table[3]/tbody/tr")[2:]

            for element in elements:
                columns = element.find_elements_by_xpath(".//td")
                name = columns[0].find_element_by_xpath(".//a").text
                link = columns[0].find_element_by_xpath(".//a").get_attribute('href')
                id = link[link.find("=") + 1:]
                status = columns[1].text
                view_status = columns[3].text
                description = columns[4].text
                self.project_cache.append(Project(name=name, status=status, view_status=view_status,
                                                  description=description, id=id))
        return list(self.project_cache)

    def delete_project_by_index(self, index):
        wd = self.app.wd
        self.open_projects_management_page()
        elements = wd.find_elements_by_xpath("/html/body/table[3]/tbody/tr")[2:]
        elements[index].find_element_by_xpath(".//td//a").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # confirmation of deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_management_page()
        wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % id).click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # confirmation of deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None

    def truncate_whitespaces(self, s):
        cleared_str = re.sub("\s+", " ", s)
        cleared_str = cleared_str.strip()
        return cleared_str
