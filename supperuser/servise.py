from org_admin.models import Organisation_admin
from hr.models import HR
from accountant.models import Accountent
from teamlead.models import TeamLead
from employee.models import Employee

def delete_organisation_with_all(org):

    Organisation_admin.objects.filter(organization=org).delete()
    HR.objects.filter(organization=org).delete()
    Employee.objects.filter(organization=org).delete()
    Accountent.objects.filter(organization=org).delete()
    TeamLead.objects.filter(organization=org).delete()
    

    org.delete()