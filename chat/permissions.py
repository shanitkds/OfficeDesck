from attendance.services import get_organisation

def same_organisation(user1,user2):
    org1=get_organisation(user1)
    org2=get_organisation(user2)
    
    if not org1 or not org2:
        return False
    
    return org1.id==org2.id

def can_private_chat(sender,receiver):
    rules={
        "EMPLOYEE": ["TEAM_LEAD", "HR"],
        "TEAM_LEAD": ["EMPLOYEE", "HR", "ORG_ADMIN"],
        "HR": ["EMPLOYEE", "TEAM_LEAD", "ACCOUNTANT", "ORG_ADMIN"],
        "ACCOUNTANT": ["HR", "ORG_ADMIN"],
        "ORG_ADMIN": ["EMPLOYEE", "TEAM_LEAD", "HR", "ACCOUNTANT"],
    }
    
    return receiver.user_type in rules.get(sender.user_type,[])

def can_create_group(user):
    return user.user_type == 'TEAM_LEAD'

def can_add_employee_to_group(team_lead_user, employee_user):
    if employee_user.user_type != "EMPLOYEE":
        return False

    return (
        employee_user.employee.team_lead.user_id == team_lead_user.id
    )