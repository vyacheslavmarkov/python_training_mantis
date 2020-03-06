from model.project import Project
import random


def test_add_project(app):
    old_projects = app.project.get_projects_list()
    if len(old_projects) == 0:
        app.project.create_simple_project()
        old_projects = app.project.get_projects_list()

    project = random.choice(old_projects)
    index = old_projects.index(project)
    app.project.delete_project_by_index(index)
    old_projects.remove(project)
    new_projects = app.project.get_projects_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
