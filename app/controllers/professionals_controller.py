from flask import jsonify, request, current_app
from app.models.professionals_model import ProfessionalsModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from psycopg2.errors import NotNullViolation
import re

# criar profissional
def create_professional():
    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'specialty', 'address']
    data = request.json

    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"msg": "Fields must be strings"}, 422

    for key in required_keys:
        if key not in data:
            return {"msg": f"Key {key} is missing"}, 400

    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
        return {"msg": "Invalid email"}, 400

    if not re.fullmatch(r'\(\d{2,}\)\d{4,}\-\d{4}', data['phone']):
        return {"msg": "Invalid phone number. Correct format: (xx)xxxxx-xxxx"}, 400

    if not re.fullmatch(r'[0-9]{3,5}-[A-Z]{2}', data['council_number']):
        return {"msg": "Invalid council number"}, 400

    try:
        new_professional = ProfessionalsModel(**data)
        current_app.db.session.add(new_professional)
        current_app.db.session.commit()
        return jsonify(new_professional), 201
    except IntegrityError:
        return {'msg': "User already exists"}, 400


# busca de todos od profissionais
def get_all_professionals():
    professionals = (ProfessionalsModel.query.all())
    result = [
        {
            "council_number": professional.council_number,
            "name": professional.name,
            "email": professional.email,
            "phone": professional.phone,
            "password": professional.password,
            "specialty": professional.specialty,
            "address": professional.address
        } for professional in professionals
    ]

    return jsonify(result)


# busca por uma especialidade especifica
def filter_by_specialty(specialty):
    professionals = (ProfessionalsModel.query.filter_by(specialty=specialty))

    result = [
        {
            "council_number": professional.council_number,
            "name": professional.name,
            "email": professional.email,
            "phone": professional.phone,
            "password": professional.password,
            "specialty": professional.specialty,
            "address": professional.address
        } for professional in professionals
    ]

    if len(result) < 1:
        return {"msg": f"No {specialty} found"}, 404

    return jsonify(result)


# atualiza os dados do profissional
def update_professional(cod):
    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'specialty', 'address']
    data = request.json

    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"msg": "Fields must be strings"}, 422

    professional = ProfessionalsModel.query.filter_by(
        council_number=cod).update(data)

    current_app.db.session.commit()

    updated_professional = ProfessionalsModel.query.get(cod)

    if updated_professional:
        return jsonify(updated_professional), 200
    return {"msg": "Professional not found"}, 404


# deleta um profissional
def delete_professional(cod: str):
    try:
        professional = ProfessionalsModel.query.filter_by(council_number=cod).first()
        current_app.db.session.delete(professional)
        current_app.db.session.commit()
        return {} , 204
    except UnmappedInstanceError:
        return {"message": "Professional not found"} , 404


