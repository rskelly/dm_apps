from django.conf import settings
from django.template import loader

from_email = settings.SITE_FROM_EMAIL

class ProjectSubmissionEmail:
    def __init__(self, object):
        if object.submitted:
            self.subject = 'A project has been submitted under your section / Un projet a été soumis dans votre section'
        else:
            self.subject = 'A project has been unsubmitted from your section / Un projet a été annulé dans votre section'

        self.message = self.load_html_template(object)
        self.from_email = from_email
        try:
            self.to_list = [object.section.head.email]
        except AttributeError:
            self.to_list = ["david.fishman@dfo-mpo.gc.ca"]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, object):
        t = loader.get_template('projects/email_project_submitted.html')

        project_field_list = [
            'id',
            'project_title',
            'section',
            'project_leads|project_leads',
        ]
        context = {'object': object, 'field_list':project_field_list}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered



class UserCreationEmail:
    def __init__(self, object):

        self.subject = 'DM Apps account creation / Création de compte DM Apps'
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = []

        try:
            self.to_list.append(object.email)
        except AttributeError:
            self.to_list.append("david.fishman@dfo-mpo.gc.ca")

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, object):
        t = loader.get_template('projects/email_user_creation.html')
        context = {'object': object,}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered
