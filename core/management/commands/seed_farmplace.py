from django.core.management.base import BaseCommand
from courses.models import CourseCategory
from ebooks.models import EbookCategory
from chicks.models import ChickType, ChickBatch
from consultancy.models import ConsultationService
from membership.models import MembershipPlan
from blog.models import ArticleCategory


class Command(BaseCommand):
    help = 'Seed the database with all categories, services, and plans from the FarmPlace document'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding FarmPlace database...\n'))

        self.seed_course_categories()
        self.seed_ebook_categories()
        self.seed_chick_types()
        self.seed_consultancy_services()
        self.seed_membership_plans()
        self.seed_blog_categories()

        self.stdout.write(self.style.SUCCESS('\nDone! All data seeded successfully.'))

    def seed_course_categories(self):
        categories = [
            {'name': 'Poultry Farming', 'slug': 'poultry-farming', 'icon': 'bi-egg', 'order': 1},
            {'name': 'Pig Farming', 'slug': 'pig-farming', 'icon': 'bi-heart', 'order': 2},
            {'name': 'Rabbit Farming', 'slug': 'rabbit-farming', 'icon': 'bi-heart', 'order': 3},
            {'name': 'Goat & Sheep Farming', 'slug': 'goat-sheep-farming', 'icon': 'bi-heart', 'order': 4},
            {'name': 'Dairy & Beef Farming', 'slug': 'dairy-beef-farming', 'icon': 'bi-cup', 'order': 5},
            {'name': 'Onion Farming', 'slug': 'onion-farming', 'icon': 'bi-flower1', 'order': 6},
            {'name': 'Vegetable Farming', 'slug': 'vegetable-farming', 'icon': 'bi-flower2', 'order': 7},
            {'name': 'Watermelon Farming', 'slug': 'watermelon-farming', 'icon': 'bi-flower1', 'order': 8},
            {'name': 'Organic Farming', 'slug': 'organic-farming', 'icon': 'bi-leaf', 'order': 9},
            {'name': 'Hydroponic Fodder', 'slug': 'hydroponic-fodder', 'icon': 'bi-water', 'order': 10},
            {'name': 'Agrimarketing', 'slug': 'agrimarketing', 'icon': 'bi-graph-up', 'order': 11},
            {'name': 'Farm Record Keeping', 'slug': 'farm-record-keeping', 'icon': 'bi-journal-text', 'order': 12},
        ]

        for cat_data in categories:
            cat, created = CourseCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Course Category: {cat.name}')

    def seed_ebook_categories(self):
        categories = [
            {'name': 'Poultry', 'slug': 'ebook-poultry', 'icon': 'bi-egg', 'order': 1},
            {'name': 'Pig', 'slug': 'ebook-pig', 'icon': 'bi-heart', 'order': 2},
            {'name': 'Rabbit', 'slug': 'ebook-rabbit', 'icon': 'bi-heart', 'order': 3},
            {'name': 'Goat', 'slug': 'ebook-goat', 'icon': 'bi-heart', 'order': 4},
            {'name': 'Dairy', 'slug': 'ebook-dairy', 'icon': 'bi-cup', 'order': 5},
            {'name': 'Crops', 'slug': 'ebook-crops', 'icon': 'bi-flower1', 'order': 6},
            {'name': 'Marketing', 'slug': 'ebook-marketing', 'icon': 'bi-graph-up', 'order': 7},
            {'name': 'Business Planning', 'slug': 'ebook-business-planning', 'icon': 'bi-briefcase', 'order': 8},
            {'name': 'Record Keeping', 'slug': 'ebook-record-keeping', 'icon': 'bi-journal-text', 'order': 9},
        ]

        for cat_data in categories:
            cat, created = EbookCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] eBook Category: {cat.name}')

    def seed_chick_types(self):
        types = [
            {
                'name': 'kenbro',
                'description': 'Hardy dual-purpose breed suitable for both meat and eggs. Known for disease resistance and adaptability to various climates.',
            },
            {
                'name': 'sasso',
                'description': 'Improved indigenous breed. Excellent for free-range systems with good foraging ability. Produces quality meat and eggs.',
            },
            {
                'name': 'sussex',
                'description': 'Excellent layers with good body weight. Popular for commercial egg production with reliable laying capacity.',
            },
        ]

        ages = [
            ('day_old', 'Day-old'),
            ('one_week', '1 Week'),
            ('two_weeks', '2 Weeks'),
            ('three_weeks', '3 Weeks'),
            ('one_month', '1 Month'),
        ]

        for type_data in types:
            chick_type, created = ChickType.objects.get_or_create(
                name=type_data['name'],
                defaults={'description': type_data['description']},
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Chick Type: {chick_type.get_name_display()}')

            for age_val, age_label in ages:
                batch, created = ChickBatch.objects.get_or_create(
                    chick_type=chick_type,
                    age=age_val,
                    batch_code=f'{type_data["name"].upper()[:3]}-{age_val[:3].upper()}',
                    defaults={
                        'quantity_available': 500,
                        'price_per_bird': self._get_price(type_data['name'], age_val),
                        'is_active': True,
                    },
                )
                status = 'CREATED' if created else 'EXISTS'
                self.stdout.write(f'    [{status}] Batch: {age_label} @ KES {batch.price_per_bird}')

    def _get_price(self, breed, age):
        base_prices = {
            'kenbro': 350,
            'sasso': 400,
            'sussex': 380,
        }
        age_multipliers = {
            'day_old': 1.0,
            'one_week': 1.3,
            'two_weeks': 1.6,
            'three_weeks': 2.0,
            'one_month': 2.5,
        }
        base = base_prices.get(breed, 350)
        multiplier = age_multipliers.get(age, 1.0)
        return base * multiplier

    def seed_consultancy_services(self):
        services = [
            {'name': 'poultry', 'description': 'Expert poultry management advice covering housing, nutrition, disease prevention, vaccination schedules, and marketing strategies.', 'price': 5000, 'duration': '2 hours', 'icon': 'bi-egg', 'order': 1},
            {'name': 'piggery', 'description': 'Complete piggery setup guidance including housing design, breed selection, feeding programs, and waste management.', 'price': 8000, 'duration': 'Half day', 'icon': 'bi-house-gear', 'order': 2},
            {'name': 'rabbit', 'description': 'Rabbit farming consultancy covering housing, breeding programs, feeding, and market development.', 'price': 4000, 'duration': '2 hours', 'icon': 'bi-heart', 'order': 3},
            {'name': 'goat', 'description': 'Goat and sheep farming guidance including breed selection, nutrition, health management, and breeding.', 'price': 5000, 'duration': '2 hours', 'icon': 'bi-heart', 'order': 4},
            {'name': 'dairy', 'description': 'Dairy management consultancy covering cow selection, feeding, milking hygiene, and milk marketing.', 'price': 6000, 'duration': 'Half day', 'icon': 'bi-cup', 'order': 5},
            {'name': 'vegetable', 'description': 'Vegetable production consultancy covering land preparation, crop selection, pest management, and market linkage.', 'price': 4000, 'duration': '2 hours', 'icon': 'bi-flower2', 'order': 6},
            {'name': 'business', 'description': 'Farm business planning including feasibility studies, business plans, financial projections, and market analysis.', 'price': 10000, 'duration': '1 day', 'icon': 'bi-briefcase', 'order': 7},
            {'name': 'biosecurity', 'description': 'Biosecurity planning to protect your farm from disease outbreaks. Includes protocols, facility design, and staff training.', 'price': 7000, 'duration': 'Half day', 'icon': 'bi-shield-check', 'order': 8},
            {'name': 'farm_visit', 'description': 'On-site farm visit for assessment, troubleshooting, and personalized recommendations.', 'price': 15000, 'duration': '1 day', 'icon': 'bi-geo-alt', 'order': 9},
            {'name': 'staff_training', 'description': 'Professional training for farm staff on best practices, biosecurity, and daily management routines.', 'price': 20000, 'duration': '1-2 days', 'icon': 'bi-people', 'order': 10},
        ]

        for svc_data in services:
            service, created = ConsultationService.objects.get_or_create(
                name=svc_data['name'],
                defaults={
                    'description': svc_data['description'],
                    'price': svc_data['price'],
                    'duration': svc_data['duration'],
                    'icon': svc_data['icon'],
                    'order': svc_data['order'],
                    'is_active': True,
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Consultancy: {service.get_name_display()}')

    def seed_membership_plans(self):
        plans = [
            {
                'name': 'Monthly Membership',
                'slug': 'monthly',
                'price': 100,
                'duration_days': 30,
                'order': 1,
                'features': [
                    'Weekly learning nuggets',
                    'Exclusive training notes',
                    'Disease alerts',
                    'Market updates',
                    'Members-only resources',
                    'Discounted courses',
                    'Monthly Q&A sessions',
                ],
            },
            {
                'name': 'Annual Membership',
                'slug': 'annual',
                'price': 1000,
                'duration_days': 365,
                'order': 2,
                'features': [
                    'Weekly learning nuggets',
                    'Exclusive training notes',
                    'Disease alerts',
                    'Market updates',
                    'Members-only resources',
                    'Discounted courses',
                    'Monthly Q&A sessions',
                    'FREE 1 course worth KES 2,500',
                    'Priority WhatsApp support',
                    'Farm assessment report',
                ],
            },
        ]

        for plan_data in plans:
            features = plan_data.pop('features')
            plan, created = MembershipPlan.objects.get_or_create(
                slug=plan_data['slug'],
                defaults={**plan_data, 'features': features},
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Membership Plan: {plan.name} @ KES {plan.price}')

    def seed_blog_categories(self):
        categories = [
            {'name': 'Poultry', 'slug': 'blog-poultry', 'icon': 'bi-egg', 'order': 1},
            {'name': 'Pig Farming', 'slug': 'blog-pig', 'icon': 'bi-heart', 'order': 2},
            {'name': 'Rabbit Farming', 'slug': 'blog-rabbit', 'icon': 'bi-heart', 'order': 3},
            {'name': 'Goat & Sheep', 'slug': 'blog-goat', 'icon': 'bi-heart', 'order': 4},
            {'name': 'Dairy', 'slug': 'blog-dairy', 'icon': 'bi-cup', 'order': 5},
            {'name': 'Crops', 'slug': 'blog-crops', 'icon': 'bi-flower1', 'order': 6},
            {'name': 'Marketing', 'slug': 'blog-marketing', 'icon': 'bi-graph-up', 'order': 7},
            {'name': 'Farm Management', 'slug': 'blog-management', 'icon': 'bi-gear', 'order': 8},
        ]

        for cat_data in categories:
            cat, created = ArticleCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Blog Category: {cat.name}')
