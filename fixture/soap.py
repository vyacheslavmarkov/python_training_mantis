from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.client_url = "%sapi/soap/mantisconnect.php?wsdl" % app.base_url

    def can_login(self, username, password):
        client = Client(self.client_url)
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        username = self.app.config['webadmin']['username']
        password = self.app.config['webadmin']['password']
        client = Client(self.client_url)
        projects = client.service.mc_projects_get_user_accessible(username, password)
        converted_projects = []
        for project in projects:
            converted_projects.append(Project(id=project.id, name=project.name, status=project.status.name,
                                              view_status=project.view_state.name, description=project.description))
        return converted_projects
