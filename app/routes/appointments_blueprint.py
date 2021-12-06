from flask import Blueprint
from controllers.appointments_controller import get_all_appointments, get_one_appointment

bp_appointments = Blueprint(
    'bp_appointments', __name__, url_prefix='/appointments')

bp_appointments.get('/<str:cpf>')(get_by_pacient)
bp_appointments.get('/<str:council_number>')(get_by_professional)
bp_appointments.get('/<date:date>')(get_by_date)
bp_appointments.post('/wait_list')(get_not_finished)