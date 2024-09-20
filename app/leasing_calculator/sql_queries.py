from .models import Seller, LeasCalculator
from .other_utils import dadata_info_company, dadata_result
from .. import db


def create_or_update_seller_and_link_to_leas_calc(
    new_name,
    new_inn,
    new_address,
    new_phone,
    new_email,
    new_signer,
    calc_id,
    new_based_on,
    new_bank,
    new_current,
):
    """Создаем или обновляем продавца и привязываем его к LeasCalculator"""
    # Проверяем, существует ли продавец с таким ИНН
    seller: Seller = Seller.query.filter_by(inn=new_inn).first()
    dadata_info: dict = dadata_info_company(new_inn)
    ogrn = dadata_result(dadata_info)["ogrn"]
    okato = dadata_result(dadata_info)["okato"]
    kpp = dadata_result(dadata_info)["kpp"]
    reg_date = dadata_result(dadata_info)["reg_date"]
    current_account = ""

    if seller:
        # Если продавец существует, обновляем его имя, если оно изменилось
        if seller.name != new_name:
            seller.name = new_name
        if seller.address != new_address:
            seller.address = new_address
        if seller.phone != new_phone:
            seller.phone = new_phone
        if seller.email != new_email:
            seller.email = new_email
        if seller.signer != new_signer:
            seller.signer = new_signer
        if seller.based_on != new_based_on:
            seller.based_on = new_based_on
        if seller.current_account != new_current:
            seller.current_account = new_current
        db.session.commit()
    else:
        # Если продавца нет, создаем нового
        seller = Seller(
            name=new_name,
            inn=new_inn,
            ogrn=ogrn,
            okato=okato,
            kpp=kpp,
            date_of_registration=reg_date,
            address=new_address,
            phone=new_phone,
            email=new_email,
            signer=new_signer,
            based_on=new_based_on,
            current_account=current_account,
        )
        db.session.add(seller)
        db.session.commit()

    # Теперь привязываем seller_id к записи в LeasCalculator
    leas_calc = LeasCalculator.query.get(calc_id)
    if not leas_calc:
        return {"error": "LeasCalculator not found"}, 404

    leas_calc.seller_id = seller.id
    db.session.commit()

    return {"message": "Seller linked to LeasCalculator successfully"}, 200
