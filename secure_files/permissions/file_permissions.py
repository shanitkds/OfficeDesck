from secure_files.models import SecureFile,FileShare

def get_user_role(user):
    return user.user_type

def can_view_file(user,file):
    user_role=get_user_role(user)
    
    if user_role=='ORG_ADMIN':
        return True
    
    if file.owner==user:
        return True
    
    if not file.allow_view:
        return False
    
    if user_role=='TEAM_LEAD':
        if file.team_lead==user.teamlead:
            return True
        
    return FileShare.objects.filter(
        file=file,
        shared_with=user,
        can_view=True
        ).exists()
    
def can_downlaod_file(user,file):
    user_role=get_user_role(user)
    
    if user_role=='ORG_ADMIN':
        return True
    
    if file.owner==user:
        return True
    
    if not file.allow_download:
        return False
    
    if user_role=='TEAM_LEAD':
        if file.team_lead==user.teamlead:
            return True
        
    return FileShare.objects.filter(
        file=file,
        shared_with=user,
        can_download=True
    ).exists()
    
def can_share_file(user,file):
    user_role=get_user_role(user)
    
    if user_role == 'EMPLOYEE':
        return False
    
    if user_role=='ORG_ADMIN':
        return True
    
    if file.owner==user and file.allow_share:
        return True
    
    if user_role=='TEAM_LEAD':
        if file.team_lead==user.teamlead and file.allow_share:
            return True
    
        
    return False
    
def file_delete_permition(user,file):
    user_role=user.user_type
    
    if user_role=="ORG_ADMIN":
        return True
    
    if file.owner == user:
        return True
    
    if user_role=='TEAM_LEAD':
        if file.team_lead==user.teamlead :
            return True
        
    return False