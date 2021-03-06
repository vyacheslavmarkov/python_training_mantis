from model.project import Project


def test_add_project(app):
    old_projects = app.soap.get_projects_list()
    # name must be unique according to Mantis rules
    project = Project(name=app.project.random_string("name", 10), status="stable", view_status="private",
                      description=app.project.random_string("desc", 30))
    app.project.create(project)
    old_projects.append(project)
    new_projects = app.soap.get_projects_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

