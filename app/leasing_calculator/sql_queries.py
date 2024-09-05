from .models import Seller
from .. import db


def create_or_update_seller_and_link_to_leas_calc(new_name, new_inn, deal_id):
    """Создаем или обновляем продавца и привязываем его к LeasCalculator"""
    # Проверяем, существует ли продавец с таким ИНН
    seller = Seller.query.filter_by(inn=new_inn).first()

    if seller:
        # Если продавец существует, обновляем его имя, если оно изменилось
        if seller.name != new_name:
            seller.name = new_name
            db.session.commit()
    else:
        # Если продавца нет, создаем нового
        seller = Seller(name=new_name, inn=new_inn)
        db.session.add(seller)
        db.session.commit()

    # # Теперь привязываем seller_id к записи в LeasCalculator
    # leas_calc = LeasCalculator.query.get(calc_id)
    # if not leas_calc:
    #     return {"error": "LeasCalculator not found"}, 404
    #
    # leas_calc.seller_id = seller.id
    # db.session.commit()

    return {"message": "Seller linked to LeasCalculator successfully"}, 200
