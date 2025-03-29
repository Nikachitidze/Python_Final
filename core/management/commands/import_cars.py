import csv
from django.core.management.base import BaseCommand
from core.models import Car, CustomUser

class Command(BaseCommand):
    help = "Import cars from CSV file"

    def handle(self, *args, **kwargs):
        # გამოიყენე სუპერიუზერი როგორც added_by
        user = CustomUser.objects.first()

        with open('media/csv/cars.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                Car.objects.create(
                    brand=row['brand'],
                    model=row['model'],
                    year=row['year'],
                    price_per_day=row['price_per_day'],
                    capacity=row['capacity'],
                    transmission=row['transmission'],
                    city=row['city'],
                    fuel_capacity=row['fuel_capacity'],
                    added_by=user,
                    photo1='cars/default.jpg',
                    photo2='cars/default.jpg',
                    photo3='cars/default.jpg'
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} მანქანა წარმატებით აიმპორტდა."))