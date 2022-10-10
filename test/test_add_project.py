from model.project import Project

def test_add_project(app, json_project):
    project = json_project
    project_list_old = app.session.get_project_list()
    if project in project_list_old:
        app.session.delete_project(project)
        project_list_old.remove(project)
    project_list_old = app.session.get_project_list()
    app.session.create_project(project)
    project_list_new = app.session.get_project_list()
    project_list_old.append(project)
    assert sorted(project_list_old, key=Project.id_or_max) == sorted(project_list_new, key=Project.id_or_max)

#
# def test_del_project(app):
#     app.session.login('administrator', 'root')
#     assert app.session.is_logged_in_as('administrator')
#     project_list = app.session.get_prohject_list()
#     chosen_project = random.choice(project_list)
#     app.session.del_project_by_index(chosen_project)

