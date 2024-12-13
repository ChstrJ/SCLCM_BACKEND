import csv
from django.core.management.base import BaseCommand
from api.models import CareerTracking

class Command(BaseCommand):
    help = 'Import dataset into CareerTracking model'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\ACER\Documents\GitHub\SCLCM_BACKEND\api\management\commands\data\CAREER-TRACKING.csv'  # Adjust the file path

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Create CareerTracking instance from row data
                        CareerTracking.objects.create(
                            name=row['Name'],
                            grade=row['Grade'],
                            section=row['Section'],
                            cle=row['CLE'],
                            english=row['English'],
                            filipino=row['Filipino'],
                            ap=row['AP'],
                            science=row['Science'],
                            math=row['Math'],
                            mapeh=row['MAPEH'],
                            tle=row['TLE'],
                            computer=row['Computer'],
                            fl=row['Foreign Language'],
                            academic_track=row['Academic Track'],
                            other_track=row['Other Track'],
                            tech_voc=row['Technical Vocation'],
                            other_techvoc=row['Other Technical Vocation'],
                            preferredCourse=row['Preferred Course'],
                            medical_records=row['Medical Records'],
                            specify=row['Specify'],
                            academic_status=row['Academic Status'],
                            hobbies=row['Hobbies'],
                            cognitive=row['Cognitive'],
                            emotional=row['Emotional'],
                            personality=row['Personality']
                        )

                        self.stdout.write(self.style.SUCCESS(f"Successfully imported data for: {row['Name']}"))

                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"An error occurred for row {row['Name']}: {e}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File '{file_path}' not found."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
