import uuid
from .models import Oganisation,OrganizationRequest
from account.models import User
from org_admin.models import Organisation_admin
from org_admin.serializers import copy_file

def create_org_and_admin_from_request(req: OrganizationRequest):

    registration_doc = copy_file(req.registration_doc) if req.registration_doc else None
    photo = copy_file(req.admin_photo) if req.admin_photo else None
    id_proof = copy_file(req.admin_id_proof) if req.admin_id_proof else None

    organisation = Oganisation.objects.create(
        name=req.org_name,
        email=req.org_email,
        phone=req.org_phone,
        address=req.org_address,
        registration_doc=registration_doc,
        registration_number=req.registration_number,
        latitude=req.latitude,
        longitude=req.longitude,
        attendance_mode=req.attendance_mode,
        full_day_last_time=req.full_day_last_time,
        half_day_cutoff_time=req.half_day_cutoff_time,
    )

    admin_employee_id = f"ADM-{uuid.uuid4().hex[:8]}"

    user = User.objects.create(
        name=req.admin_name,
        email=req.admin_email,
        employee_id=admin_employee_id,
        user_type="ORG_ADMIN",
        phone=req.admin_phone,
    )
    
    user.password = req.admin_password   
    user.save()

    Organisation_admin.objects.create(
        user=user,
        organization=organisation,
        photo=photo,
        id_proof=id_proof
    )

    return organisation