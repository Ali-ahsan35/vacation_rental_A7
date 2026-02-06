"""
CSV Import Management Command

WHAT THIS FILE DOES:
- Custom Django command to import properties from CSV
- Run with: python manage.py import_properties filename.csv --skip-location
- Can import with or without location data

TOPICS TO LEARN:
- Django management commands
- CSV file handling
- Bulk data import
- Error handling
"""

import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from properties.models import Property
from locations.models import Location


class Command(BaseCommand):
    """
    Import properties from a CSV file
    
    USAGE:
    python manage.py import_properties data/properties.csv
    python manage.py import_properties data/properties_no_location.csv --skip-location
    """
    
    help = 'Import properties from a CSV file'
    # EXPLANATION: This text shows when you run: python manage.py help import_properties

    def add_arguments(self, parser):
        """
        Define command-line arguments
        
        WHAT THIS DOES:
        Defines what arguments this command accepts
        """
        # Required argument: CSV file path
        parser.add_argument(
            'csv_file', 
            type=str, 
            help='Path to the CSV file'
        )
        
        # Optional flag: --skip-location
        parser.add_argument(
            '--skip-location',
            action='store_true',
            help='Skip location validation (location must be added manually in admin)'
        )


    def handle(self, *args, **options):
        """
        Main command logic
        
        WHAT THIS DOES:
        This method runs when you execute the command
        """
        csv_file = options['csv_file']  # Get the CSV filename
        skip_location = options.get('skip_location', False)  # Get the flag
        
        # Show starting message
        self.stdout.write(
            self.style.SUCCESS(f'Starting import from {csv_file}...')
        )
        
        # Show warning if skipping location
        if skip_location:
            self.stdout.write(
                self.style.WARNING(
                    'Location validation skipped. You must assign locations manually in admin!'
                )
            )
        
        # Try to open and read the CSV file
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # EXPLANATION: DictReader reads CSV as dictionaries
                # Each row becomes: {'title': 'Villa', 'bedrooms': '3', ...}
                
                # Counters for statistics
                created_count = 0
                updated_count = 0
                error_count = 0
                
                # Process each row
                for row_num, row in enumerate(reader, start=2):
                    # EXPLANATION: start=2 because row 1 is headers
                    
                    try:
                        location = None
                        
                        # ========== HANDLE LOCATION ==========
                        if not skip_location:
                            # Get location data from CSV
                            location_name = row.get('location', '').strip()
                            city = row.get('city', '').strip()
                            state = row.get('state', '').strip()
                            country = row.get('country', 'USA').strip()
                            
                            # Check if location data is present
                            if not location_name or not city or not state:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'Row {row_num}: Missing location data, skipping...'
                                    )
                                )
                                error_count += 1
                                continue
                            
                            # Get or create location
                            location, created = Location.objects.get_or_create(
                                name=location_name,
                                defaults={
                                    'city': city,
                                    'state': state,
                                    'country': country
                                }
                            )
                           
                        else:
                            location = None
                        
                        
                        # ========== GET PROPERTY DATA ==========
                        title = row.get('title', '').strip()
                        
                        if not title:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Row {row_num}: Missing title, skipping...'
                                )
                            )
                            error_count += 1
                            continue
                        
                        
                        # ========== PARSE NUMERIC FIELDS ==========
                        # Use try-except to handle invalid numbers
                        
                        try:
                            bedrooms = int(row.get('bedrooms', 1))
                        except (ValueError, TypeError):
                            bedrooms = 1  # Default value
                        
                        try:
                            bathrooms = Decimal(row.get('bathrooms', '1.0'))
                        except (ValueError, TypeError):
                            bathrooms = Decimal('1.0')
                        
                        try:
                            max_guests = int(row.get('max_guests', 2))
                        except (ValueError, TypeError):
                            max_guests = 2
                        
                        try:
                            price_per_night = Decimal(row.get('price_per_night', '100.00'))
                        except (ValueError, TypeError):
                            price_per_night = Decimal('100.00')
                        
                        
                        # ========== PREPARE PROPERTY DATA ==========
                        property_data = {
                            'description': row.get('description', '').strip(),
                            'property_type': row.get('property_type', '').strip(),
                            'bedrooms': bedrooms,
                            'bathrooms': bathrooms,
                            'max_guests': max_guests,
                            'price_per_night': price_per_night,
                            'address': row.get('address', '').strip(),
                            'amenities': row.get('amenities', '').strip(),
                            'is_available': row.get('is_available', 'true').lower() == 'true',
                        }
                        
                        # Add location if available
                        if location:
                            property_data['location'] = location
                        
                        
                        # ========== CREATE OR UPDATE PROPERTY ==========
                        if skip_location or not location:
                            # Create new property without location
                            property_obj = Property.objects.create(
                                title=title,
                                **property_data  # Unpack dictionary
                            )
                            created_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Row {row_num}: Created property "{title}" (Location needed in admin)'
                                )
                            )
                        else:
                            # Update or create with location
                            property_obj, created = Property.objects.update_or_create(
                                title=title,
                                location=location,
                                defaults=property_data
                            )
                    
                            if created:
                                created_count += 1
                                self.stdout.write(f'Row {row_num}: Created property "{title}"')
                            else:
                                updated_count += 1
                                self.stdout.write(f'Row {row_num}: Updated property "{title}"')
                    
                    except Exception as e:
                        # Catch any errors for this row
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'Row {row_num}: Error processing row - {str(e)}'
                            )
                        )
                
                
                # ========== SUMMARY ==========
                self.stdout.write(self.style.SUCCESS('\n' + '='*50))
                self.stdout.write(self.style.SUCCESS('Import Summary:'))
                self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
                self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
                if error_count > 0:
                    self.stdout.write(self.style.WARNING(f'Errors: {error_count}'))
                self.stdout.write(self.style.SUCCESS('='*50))
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading CSV file: {str(e)}')
            )

