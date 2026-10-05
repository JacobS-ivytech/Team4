from django.core.management.base import BaseCommand

from OrderApp.models import Category, MenuItem


MENU = {
    "Appetizers": [
        ("Carne y Papas", "Ancho chile-crusted beef tips, potatoes, smoky Peruvian aioli", 15.00, "carne_y_papas.jpg"),
        ("Guacamole", "Made fresh daily, served with tortilla chips", 9.00, "guacamole.jpg"),
        ("Elote", "Grilled corn with queso fresco, cilantro, mayo, Cholula, ancho chile", 5.00, "elote.jpg"),
        ("Na-cho Last Lunch", "Chicken tinga, olive tapenade, crema, pickled onions", 9.00, "nacho_last_lunch.jpg"),
        ("Sweet Corn Tamale", "Pepitas and buckwheat honey", 4.00, "sweet_corn_tamale.jpg"),
        ("Yuca Fries", "Fried yuca with chimichurri pesto and aioli", 7.00, "yuca_fries.jpg"),
        ("Lamb Empanada (One)", "Fried pastry filled with braised lamb shoulder", 12.00, "lamb_empanada.jpg"),
        ("Lamb Empanada (Two)", "Fried pastry filled with braised lamb shoulder", 19.00, ""),
        ("Mayan Pozole Soup (Cup)", "Yucatan-style slow-roasted pork, napa cabbage", 7.00, ""),
        ("Mayan Pozole Soup (Bowl)", "Yucatan-style slow-roasted pork, napa cabbage", 14.00, "mayan_pozole.jpg"),
    ],

    "Salads": [
        ("Manzana Salad", "Gem lettuce, watermelon radish, apple, queso fresco, peanuts", 9.00, "manzana_salad.jpg"),
        ("Peruvian Caesar Salad", "Grilled romaine, queso fresco, yuca croutons", 9.00, "peruvian_caesar.jpg"),
    ],

    "Sides": [
        ("Incan Rice", "", 5.00, ""),
        ("Refried Beans", "", 4.00, ""),
        ("Peruvian Caesar", "", 5.00, ""),
        ("Manzana Salad (Side)", "", 5.00, ""),
    ],

    "Sauces": [
        ("Chipotle Aioli", "", 5.00, ""),
        ("Red Pepper Aioli", "", 5.00, ""),
        ("Pineapple Chimichurri", "", 5.00, ""),
        ("Chimichurri", "", 6.00, ""),
        ("Passionfruit & Habanero", "", 6.00, ""),
    ],

    "Street Tacos, Burritos & Bowls": [
        ("Campechano - Street Taco", "Bourbon & butcher chorizo, crispy pork belly", 6.00, "campechano.jpg"),
        ("Campechano - Burrito", "Bourbon & butcher chorizo, crispy pork belly", 13.00, ""),
        ("Campechano - Bowl", "Bourbon & butcher chorizo, crispy pork belly", 16.00, ""),

        ("Lamb Birria - Street Taco", "Slow-roasted lamb", 5.50, "lamb_birria.jpg"),
        ("Lamb Birria - Burrito", "Slow-roasted lamb", 12.50, ""),
        ("Lamb Birria - Bowl", "Slow-roasted lamb", 16.00, ""),

        ("Maria Sabina - Street Taco", "Sauteed beech mushrooms", 5.50, "maria_sabina.jpg"),
        ("Maria Sabina - Burrito", "Sauteed beech mushrooms", 12.50, ""),
        ("Maria Sabina - Bowl", "Sauteed beech mushrooms", 15.50, ""),

        ("Mezcal Shrimp - Street Taco", "Mezcal glazed, fire-roasted", 6.50, "mezcal_shrimp.jpg"),
        ("Mezcal Shrimp - Burrito", "Mezcal glazed, fire-roasted", 13.50, ""),
        ("Mezcal Shrimp - Bowl", "Mezcal glazed, fire-roasted", 16.50, ""),

        ("Chicken Tinga - Street Taco", "Slow-braised in tomato chipotle sauce", 5.50, "chicken_tinga.jpg"),
        ("Chicken Tinga - Burrito", "Slow-braised in tomato chipotle sauce", 12.50, ""),
        ("Chicken Tinga - Bowl", "Slow-braised in tomato chipotle sauce", 15.50, ""),

        ("Carne Asada - Street Taco", "Anticucho marinated strip steak", 6.50, "carne_asada.jpg"),
        ("Carne Asada - Burrito", "Anticucho marinated strip steak", 13.50, ""),
        ("Carne Asada - Bowl", "Anticucho marinated strip steak", 15.50, ""),

        ("Cochinita - Street Taco", "Traditional Yucatan-style slow-roasted pork", 5.50, "cochinita.jpg"),
        ("Cochinita - Burrito", "Traditional Yucatan-style slow-roasted pork", 12.50, ""),
        ("Cochinita - Bowl", "Traditional Yucatan-style slow-roasted pork", 15.50, ""),
    ],

    "Add-ons": [
        ("Peruvian Street Chicken (Add-on)", "Salad protein add-on", 6.00, ""),
        ("Mezcal Glazed Shrimp, Two (Add-on)", "Salad protein add-on", 10.00, ""),
        ("Dark Honey Braised Pork Belly (Add-on)", "Salad protein add-on", 7.00, ""),
        ("Carne Asada (Add-on)", "Salad protein add-on", 10.00, ""),
        ("Extra Side with Mix & Match Tacos", "Two or more tacos, add a side", 3.00, ""),
        ("Wet Burrito", "Any burrito smothered in aji amarillo queso", 3.00, ""),
        ("Burrito with Side", "", 3.00, ""),
    ],
}


class Command(BaseCommand):
    help = "Seed the database with the Jesus Latin Grill lunch menu categories and items"

    def handle(self, *args, **options):
        for order, (category_name, items) in enumerate(MENU.items()):
            category, _ = Category.objects.update_or_create(
                name=category_name,
                defaults={"display_order": order},
            )

            for name, description, price, image_filename in items:
                image_path = (
                    f"menu_images/{image_filename}"
                    if image_filename
                    else ""
                )

                MenuItem.objects.update_or_create(
                    category=category,
                    name=name,
                    defaults={
                        "description": description,
                        "price": price,
                        "image": image_path,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Menu seeded successfully.")
        )