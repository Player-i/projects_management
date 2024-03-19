from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_project_manager = models.BooleanField(default=False)
    manager = models.CharField(max_length=255, blank=True, null=True)
    assigned_steps_count = models.BigIntegerField(default=0)
    completed_steps_count = models.BigIntegerField(default=0)
    progress_percentage = models.BigIntegerField(default=0)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        permissions = [
            ("can_create_users", "Can create new users"),
        ]

class Job(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)


    
    def __str__(self):
        return self.name


class Project(models.Model):
    job = models.ForeignKey(Job,  on_delete=models.CASCADE )
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    description = models.TextField()
    equipment = models.TextField(blank=True)
    vehicle = models.TextField(blank=True)
    todays_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="") 
    description = models.TextField(null=True, blank=True, default="")
    todays_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    assigned_to = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to="static/steps/", null=True, blank=True)
    file2 = models.FileField(upload_to="static/steps/", null=True, blank=True)
    file3 = models.FileField(upload_to="static/steps/", null=True, blank=True)
    file4 = models.FileField(upload_to="static/steps/", null=True, blank=True)
    sign_sheet = models.FileField(upload_to="static/steps/", null=True, blank=True)

    def __str__(self):
        return self.name

class Budget(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    initial_budget = models.BooleanField(default=False)

    # Additional JSON fields for each cost code
    architecture_mep_egr = models.JSONField(default=dict(cost_code="300.00000", name="Architecture/MEP EGR", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    engineering_surveying = models.JSONField(default=dict(cost_code="310.00000", name="Engineering/Surveying", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    town_review_fees = models.JSONField(default=dict(cost_code="320.00000", name="Town Review Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    studies = models.JSONField(default=dict(cost_code="350.00000", name="Studies", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    estimating_bidding = models.JSONField(default=dict(cost_code="400.00000", name="Estimating & Bidding", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    administration_fees = models.JSONField(default=dict(cost_code="610.00000", name="Administration Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    commission_expense = models.JSONField(default=dict(cost_code="710.00000", name="Commission Expense", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    settlement_fees = models.JSONField(default=dict(cost_code="720.00000", name="Settlement Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    legal_fees = models.JSONField(default=dict(cost_code="730.00000", name="Legal Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    accounting_fees = models.JSONField(default=dict(cost_code="750.00000", name="Accounting Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    marketing_expense = models.JSONField(default=dict(cost_code="760.00000", name="Marketing Expense", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    permits_fees = models.JSONField(default=dict(cost_code="890.90000", name="Permits & Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    utility_fees = models.JSONField(default=dict(cost_code="900.00000", name="Utility Fees", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    management_fee = models.JSONField(default=dict(cost_code="1,000.00000", name="Management Fee", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    administration_requirements = models.JSONField(default=dict(cost_code="1,300.00000", name="Administration Requirements", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    project_management_supervision = models.JSONField(default=dict(cost_code="1,310.00000", name="Project Management/Supervision", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    testing_inspection = models.JSONField(default=dict(cost_code="1,450.00000", name="Testing & Inspection", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    temporary_facilities_control = models.JSONField(default=dict(cost_code="1,500.00000", name="Temporary Facilities & Control", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    execution_requirements = models.JSONField(default=dict(cost_code="1,700.00000", name="Execution Requirements", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    surveying_field_docs = models.JSONField(default=dict(cost_code="1,720.00000", name="Surveying & Field Docs", materials=0, labor=0, equipment=0, subcontract=0, other=0))

    pest_control = models.JSONField(default=dict(cost_code="1,730.00000", name="Pest Control", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    dumpsters_construction_cleaning = models.JSONField(default=dict(cost_code="1,740.00000", name="Dumpsters/Construction Cleaning", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    final_cleaning = models.JSONField(default=dict(cost_code="1,745.00000", name="Final Cleaning", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    punchlist_tools_equip = models.JSONField(default=dict(cost_code="1,800.00000", name="Punchlist/Tools/Equip", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    operation_maintenance = models.JSONField(default=dict(cost_code="1,830.00000", name="Operation & Maintenance", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    excavation = models.JSONField(default=dict(cost_code="2,000.00000", name="Excavation", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    site_work_materials = models.JSONField(default=dict(cost_code="2,050.00000", name="Site Work & Materials", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    asphalt_paving = models.JSONField(default=dict(cost_code="2,100.00000", name="Asphalt Paving", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    pervious_concrete = models.JSONField(default=dict(cost_code="2,150.00000", name="Pervious Concrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    temp_barricades = models.JSONField(default=dict(cost_code="2,225.00000", name="Temp Barricades", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    demolition = models.JSONField(default=dict(cost_code="2,230.00000", name="Demolition", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    paving_concrete_demo = models.JSONField(default=dict(cost_code="2,232.00000", name="Paving & Concrete Demo", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    pumping_mucking = models.JSONField(default=dict(cost_code="2,235.00000", name="Pumping & Mucking", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    erosion_sediment_control = models.JSONField(default=dict(cost_code="2,370.00000", name="Erosion & Sediment Control", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    water = models.JSONField(default=dict(cost_code="2,510.00000", name="Water", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    well = models.JSONField(default=dict(cost_code="2,520.00000", name="Well", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    sewer = models.JSONField(default=dict(cost_code="2,530.00000", name="Sewer", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    septic_system = models.JSONField(default=dict(cost_code="2,540.00000", name="Septic System", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    storm_drain_drainage = models.JSONField(default=dict(cost_code="2,600.00000", name="Storm Drain/Drainage", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    bioretention_stormwater = models.JSONField(default=dict(cost_code="2,650.00000", name="Bioretention/Stormwater", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    curb_gutter = models.JSONField(default=dict(cost_code="2,770.00000", name="Curb & Gutter", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    site_improvements_amenities = models.JSONField(default=dict(cost_code="2,800.00000", name="Site Improvements & Amenities", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    plantings = models.JSONField(default=dict(cost_code="2,900.00000", name="Plantings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    concrete = models.JSONField(default=dict(cost_code="3,000.00000", name="CONCRETE", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    concrete_construction = models.JSONField(default=dict(cost_code="3,050.00000", name="Concrete Construction", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    dig_pour_footers = models.JSONField(default=dict(cost_code="3,060.00000", name="Dig & Pour Footers", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    foundation = models.JSONField(default=dict(cost_code="3,070.00000", name="Foundation", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    slab_prep_backfill = models.JSONField(default=dict(cost_code="3,080.00000", name="Slab Prep & Backfill", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    interior_concrete = models.JSONField(default=dict(cost_code="3,100.00000", name="Interior Concrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    exterior_concrete = models.JSONField(default=dict(cost_code="3,150.00000", name="Exterior Concrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    pre_cast_concrete = models.JSONField(default=dict(cost_code="3,200.00000", name="Pre-Cast Concrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    cast_in_place_concrete = models.JSONField(default=dict(cost_code="3,300.00000", name="Cast in Place Concrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    gypcrete = models.JSONField(default=dict(cost_code="3,400.00000", name="Gypcrete", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    masonry_material_labor = models.JSONField(default=dict(cost_code="4,050.00000", name="Masonry Material & Labor", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    stone_material_labor = models.JSONField(default=dict(cost_code="4,300.00000", name="Stone Material & Labor", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    brick_material_labor = models.JSONField(default=dict(cost_code="4,350.00000", name="Brick Material & Labor", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    structural_steel = models.JSONField(default=dict(cost_code="5,100.00000", name="Structural Steel", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    metal_framing = models.JSONField(default=dict(cost_code="5,400.00000", name="Metal Framing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    metal_railings = models.JSONField(default=dict(cost_code="5,440.00000", name="Metal Railings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    metal_fabrications = models.JSONField(default=dict(cost_code="5,500.00000", name="Metal Fabrications", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    rough_carpentry_material = models.JSONField(default=dict(cost_code="6,110.00000", name="Rough Carpentry Material", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    rough_carpentry_labor = models.JSONField(default=dict(cost_code="6,120.00000", name="Rough Carpentry Labor", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    floor_trusses = models.JSONField(default=dict(cost_code="6,140.00000", name="Floor Trusses", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    structural_wood_beams = models.JSONField(default=dict(cost_code="6,145.00000", name="Structural Wood Beams", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    roof_trusses = models.JSONField(default=dict(cost_code="6,150.00000", name="Roof Trusses", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    exterior_trim_rails = models.JSONField(default=dict(cost_code="6,160.00000", name="Exterior Trim & Rails", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    trim_carpentry = models.JSONField(default=dict(cost_code="6,200.00000", name="Trim Carpentry", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    molding_millwork = models.JSONField(default=dict(cost_code="6,220.00000", name="Molding & Millwork", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    wood_stairs = models.JSONField(default=dict(cost_code="6,230.00000", name="Wood Stairs", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    interior_rails = models.JSONField(default=dict(cost_code="6,240.00000", name="Interior Rails", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    plastic_fabrications = models.JSONField(default=dict(cost_code="6,600.00000", name="Plastic Fabrications", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    foundation_waterproofing = models.JSONField(default=dict(cost_code="7,100.00000", name="Foundation Waterproofing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    thermal_protection = models.JSONField(default=dict(cost_code="7,200.00000", name="Thermal Protection", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    eifs = models.JSONField(default=dict(cost_code="7,240.00000", name="EIFS", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    insulation = models.JSONField(default=dict(cost_code="7,300.00000", name="Insulation", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    shingles_roof_coverings = models.JSONField(default=dict(cost_code="7,310.00000", name="Shingles, Roof Coverings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    vinyl_siding = models.JSONField(default=dict(cost_code="7,460.00000", name="Vinyl Siding", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    gutters_downspouts = models.JSONField(default=dict(cost_code="7,470.00000", name="Gutters & Downspouts", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    roof_curbs = models.JSONField(default=dict(cost_code="7,480.00000", name="Roof Curbs", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    membrane_roofing = models.JSONField(default=dict(cost_code="7,500.00000", name="Membrane Roofing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    membrane_decking = models.JSONField(default=dict(cost_code="7,550.00000", name="Membrane Decking", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    sheet_metal_roofing = models.JSONField(default=dict(cost_code="7,600.00000", name="Sheet Metal Roofing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    awnings = models.JSONField(default=dict(cost_code="7,700.00000", name="Awnings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fireproofing = models.JSONField(default=dict(cost_code="7,800.00000", name="Fireproofing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    caulking_joint_sealers = models.JSONField(default=dict(cost_code="7,900.00000", name="Caulking/Joint Sealers", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    open_field = models.JSONField(default=dict(cost_code="8,000.00000", name="OPEN", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    int_ext_doors = models.JSONField(default=dict(cost_code="8,100.00000", name="Int./Ext. Doors", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    exterior_doors = models.JSONField(default=dict(cost_code="8,200.00000", name="Exterior Doors", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    sliding_glass_doors = models.JSONField(default=dict(cost_code="8,250.00000", name="Sliding Glass Doors SGD", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    interior_doors = models.JSONField(default=dict(cost_code="8,300.00000", name="Interior Doors", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    entrances_storefronts = models.JSONField(default=dict(cost_code="8,400.00000", name="Entrances & Storefronts", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    windows = models.JSONField(default=dict(cost_code="8,500.00000", name="Windows", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    access_doors_hatch = models.JSONField(default=dict(cost_code="8,600.00000", name="Access Doors/Hatch", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    shower_doors = models.JSONField(default=dict(cost_code="8,650.00000", name="Shower Doors", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    door_hardware = models.JSONField(default=dict(cost_code="8,710.00000", name="Door Hardware", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    overhead_doors = models.JSONField(default=dict(cost_code="8,900.00000", name="Overhead Doors", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    drywall_gypsum = models.JSONField(default=dict(cost_code="9,200.00000", name="Drywall & Gypsum", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    tile = models.JSONField(default=dict(cost_code="9,300.00000", name="Tile", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    ceilings = models.JSONField(default=dict(cost_code="9,500.00000", name="Ceilings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    flooring = models.JSONField(default=dict(cost_code="9,600.00000", name="Flooring", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    ceramic = models.JSONField(default=dict(cost_code="9,630.00000", name="Ceramic", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    wood_flooring = models.JSONField(default=dict(cost_code="9,640.00000", name="Wood Flooring", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    resilient_flooring = models.JSONField(default=dict(cost_code="9,650.00000", name="Resilient Flooring", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    rubber_flooring = models.JSONField(default=dict(cost_code="9,660.00000", name="Rubber Flooring", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    epoxy_flooring = models.JSONField(default=dict(cost_code="9,670.00000", name="Epoxy Flooring", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    carpet_padding = models.JSONField(default=dict(cost_code="9,680.00000", name="Carpet & Padding", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    wall_finishes = models.JSONField(default=dict(cost_code="9,700.00000", name="Wall Finishes", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    frp = models.JSONField(default=dict(cost_code="9,750.00000", name="FRP", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    paint_coatings = models.JSONField(default=dict(cost_code="9,900.00000", name="Paint & Coatings", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    hardware = models.JSONField(default=dict(cost_code="10,100.00000", name="Hardware", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    wall_corner_guards = models.JSONField(default=dict(cost_code="10,260.00000", name="Wall and Corner Guards", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    window_door_blinds = models.JSONField(default=dict(cost_code="10,280.00000", name="Window & Door Blinds", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    pest_control = models.JSONField(default=dict(cost_code="10,290.00000", name="Pest Control", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fireplaces_stoves = models.JSONField(default=dict(cost_code="10,300.00000", name="Fireplaces and Stoves", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    identification_devices = models.JSONField(default=dict(cost_code="10,400.00000", name="Identification Devices", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fire_protection_specialties = models.JSONField(default=dict(cost_code="10,520.00000", name="Fire Protection Specialties", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    protective_covers = models.JSONField(default=dict(cost_code="10,530.00000", name="Protective Covers", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    mailboxes_postal_reqs = models.JSONField(default=dict(cost_code="10,550.00000", name="Mailboxes Postal Req's", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    shelving = models.JSONField(default=dict(cost_code="10,670.00000", name="Shelving", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    signage = models.JSONField(default=dict(cost_code="10,700.00000", name="Signage", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    bath_laundry_accessories = models.JSONField(default=dict(cost_code="10,800.00000", name="Bath & Laundry Accessories", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fire_extinguishers = models.JSONField(default=dict(cost_code="10,900.00000", name="Fire Extinguishers", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    water_treatment_equip = models.JSONField(default=dict(cost_code="11,200.00000", name="Water Treatment Equip", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    food_service_equipment = models.JSONField(default=dict(cost_code="11,400.00000", name="Food Service Equipment", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    appliances = models.JSONField(default=dict(cost_code="11,450.00000", name="Appliances", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    cabinetry = models.JSONField(default=dict(cost_code="12,350.00000", name="Cabinetry", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    laminate_counter_tops = models.JSONField(default=dict(cost_code="12,360.00000", name="Laminate Counter Tops", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    granite_countertops = models.JSONField(default=dict(cost_code="12,400.00000", name="Granite Countertops", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    furniture = models.JSONField(default=dict(cost_code="12,500.00000", name="Furniture", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    television = models.JSONField(default=dict(cost_code="12,600.00000", name="Television", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fire_detection_alarm = models.JSONField(default=dict(cost_code="13,850.00000", name="Fire Detection & Alarm", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    elevators = models.JSONField(default=dict(cost_code="14,200.00000", name="Elevators", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    plumbing = models.JSONField(default=dict(cost_code="15,100.00000", name="Plumbing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    plumbing_fixtures = models.JSONField(default=dict(cost_code="15,200.00000", name="Plumbing Fixtures", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    hot_water_heaters = models.JSONField(default=dict(cost_code="15,205.00000", name="Hot Water Heaters", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    sewer_water_connection = models.JSONField(default=dict(cost_code="15,207.00000", name="Sewer & Water Connection", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    gas_piping_dnu = models.JSONField(default=dict(cost_code="15,210.00000", name="Gas Piping/DNU", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    pumps = models.JSONField(default=dict(cost_code="15,220.00000", name="Pumps", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    water_meters = models.JSONField(default=dict(cost_code="15,230.00000", name="Water Meters", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    gas_piping_meters = models.JSONField(default=dict(cost_code="15,250.00000", name="Gas Piping/Meters", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    fire_sprinkler_system = models.JSONField(default=dict(cost_code="15,300.00000", name="Fire Sprinkler System", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    sprinkler_riser = models.JSONField(default=dict(cost_code="15,350.00000", name="Sprinkler Riser", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    exterior_stairs_rails = models.JSONField(default=dict(cost_code="15,500.00000", name="Exterior Stairs & Rails", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    refrigeration_equipment = models.JSONField(default=dict(cost_code="15,600.00000", name="Refrigeration Equipment", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    hvac = models.JSONField(default=dict(cost_code="15,700.00000", name="HVAC", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    ventilation = models.JSONField(default=dict(cost_code="15,720.00000", name="Ventilation", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    testing_balancing = models.JSONField(default=dict(cost_code="15,950.00000", name="Testing & Balancing", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    general_electric = models.JSONField(default=dict(cost_code="16,050.00000", name="General Electric", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    electrical_fixtures = models.JSONField(default=dict(cost_code="16,055.00000", name="Electrical Fixtures", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    conduits = models.JSONField(default=dict(cost_code="16,100.00000", name="Conduits", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    underground_electric_service = models.JSONField(default=dict(cost_code="16,200.00000", name="Underground Electric Service", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    exterior_site_lighting = models.JSONField(default=dict(cost_code="16,300.00000", name="Exterior Site Lighting", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    low_voltage = models.JSONField(default=dict(cost_code="16,400.00000", name="Low Voltage", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    communications = models.JSONField(default=dict(cost_code="16,700.00000", name="Communications", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    surveillance_cameras = models.JSONField(default=dict(cost_code="16,800.00000", name="Surveillance & Cameras", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    warranty = models.JSONField(default=dict(cost_code="25,000.00000", name="Warranty", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    warranty_bld_f = models.JSONField(default=dict(cost_code="25,001.00000", name="Warranty- Bld F", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    warranty_bld_d = models.JSONField(default=dict(cost_code="25,002.00000", name="Warranty- Bld D", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    warranty_bld_e = models.JSONField(default=dict(cost_code="25,003.00000", name="Warranty- Bld E", materials=0, labor=0, equipment=0, subcontract=0, other=0))
    access_control = models.JSONField(default=dict(cost_code="28,010.00000", name="Access Control", materials=0, labor=0, equipment=0, subcontract=0, other=0))


