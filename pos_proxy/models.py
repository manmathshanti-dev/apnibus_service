from django.db import models
import uuid
from common.models.base_model import PosBaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField






class Operator(PosBaseModel):
    CONDUCTOR = "conductor"
    BUS_GROUP = "bus_group"
    BUSINESS_HISAB_TYPE = (
        (CONDUCTOR, "Conductor"),
        (BUS_GROUP, "Bus group"),
    )

    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_hindi_name = models.CharField(max_length=100, null=True, blank=True)
    operator_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=25, null=True, blank=True, unique=True)
    is_demo_account = models.BooleanField(default=False, null=True, blank=True)
    data_fetch_date = models.JSONField(null=True, blank=True)
    gps_commission_percentage = models.IntegerField(null=True, blank=True, default=0)
    qr_gps_commission_percentage = models.IntegerField(null=True, blank=True, default=0)
    gps_deduction_enabled = models.BooleanField(default=False, null=True, blank=True)
    gps_recovery_amount = models.IntegerField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    city = models.CharField(null=True, blank=True)
    district = models.CharField(null=True, blank=True)
    state = models.CharField(null=True, blank=True)
    pincode = models.CharField(null=True, blank=True)
    operator_lat = models.DecimalField(
        max_digits=15, decimal_places=10, null=True, blank=True
    )
    operator_lng = models.DecimalField(
        max_digits=15, decimal_places=10, null=True, blank=True
    )
    dsn_cleaned = models.BooleanField(default=True, null=False, blank=False)
    hisab_locked = models.BooleanField(default=False, db_index=True)
    to_filter_services_by_time = models.BooleanField(
        default=False, null=True, blank=True
    )
    to_filter_services_by_bus_id = models.BooleanField(
        default=False, null=True, blank=True
    )

    is_conductor_selection_enabled = models.BooleanField(
        default=False, null=True, blank=True
    )

    is_bus_selection_otp_enabled = models.BooleanField(
        default=False, null=True, blank=True
    )

    first_nudge_duration_no_internet = models.BigIntegerField(
        null=True, blank=True, default=86400000
    )
    second_nudge_no_internet = models.BigIntegerField(
        null=True, blank=True, default=21600000
    )
    skipable_screen_duration_no_internet = models.BigIntegerField(
        null=True, blank=True, default=3600000
    )

    to_show_conductor_discount_in_report = models.BooleanField(
        default=False, null=True, blank=True
    )
    is_luggage_charge_enabled = models.BooleanField(
        default=False, null=True, blank=True
    )
    maxNudgesBForceUpdate = models.IntegerField(default=3, null=True, blank=True)
    global_ticket_counter_enabled = models.BooleanField(
        default=False, null=True, blank=True
    )
    new_service_filter_by_bus_id = models.BooleanField(default=False, null=True, blank=True)
    gst_discount = models.IntegerField(default=0, null=True, blank=True)

    GST_FLOW_CHOICES = [
        (1, "old gst flow"),
        (2, "gst extended flow"),
        (3, "gst_daily_payment_deduction flow"),
    ]

    gst_flow_type = models.PositiveSmallIntegerField(
        choices=GST_FLOW_CHOICES, default=1, null=True, blank=True
    )

    speedy_upload_download = models.BooleanField(default=True, null=True, blank=True)
    is_dsn_hisab_enabled= models.BooleanField(default=False, null=True, blank=True)

    ALLOWED_APPS_CHOICES = [
        ('ab_partner', 'AB_PARTNER'),
        ('ab_local', 'AB_LOCAL')
    ]

    allowed_apps = ArrayField(
        models.CharField(max_length=20, choices=ALLOWED_APPS_CHOICES),
        default=['partner'],
        null=True,
        blank=True,
        help_text="List of allowed apps for the operator"
    )

    subscription_model = models.BooleanField(default=False,null=True, blank=True)
    is_autodebit_enabled = models.BooleanField(default=False, null=True,blank=True)
    minimum_day_recharge_pos = models.IntegerField(default=7, null=True, blank=True)
    bus_hisab_type =models.CharField(
        max_length=255,
        choices=BUSINESS_HISAB_TYPE,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        managed = False
        db_table = "operators_operator"

class ProxyTrip(Operator):
    class Meta:
        proxy = True




class Route(PosBaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    pos_route_id = models.UUIDField(default=uuid.uuid4)


    class Meta:
        managed = False
        db_table = "timetable_route"

class ProxyRoute(Route):
    class Meta:
        proxy=True


class Bus(PosBaseModel):
    HINDI = "hindi"
    ENGLISH = "english"
    PUNJABI = "punjabi"
    GUJRATI = "gujrati"
    LANGUAGES = ((HINDI, "Hindi"), (ENGLISH, "English"), (PUNJABI, "Punjabi"), (GUJRATI, "Gujrati"))
    COMMISSION_VALIDATOR = [MaxValueValidator(30), MinValueValidator(0)]

    PERCENTAGE = "percentage"
    FIXED = "fixed"
    BOOKING_OFF = "booking_off"
    END_TRIP = "end_trip"
    OFFICE_REPORT = "office_report"
    OFFICE_REPORT_WITH_AMOUNT = "office_report_with_amount"

    ONLINE_APP_BOOKING_COMMISSION = (
        (PERCENTAGE, "percentage"),
        (FIXED, "fixed"),
        (BOOKING_OFF, "booking_off"),
    )

    END_TRIP_REPORT_TYPE = (
        (END_TRIP, "end_trip"),
        (OFFICE_REPORT, "office_report"),
        (OFFICE_REPORT_WITH_AMOUNT, "office_report_with_amount")
    )

    FULL_AMOUNT = "full_amount"

    QR_BOOKING_COMMISSION = ((FULL_AMOUNT, "full_amount"), (BOOKING_OFF, "booking_off"))
    bus_number = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    operator = models.ForeignKey(
        Operator,
        on_delete=models.SET_NULL,
        related_name="related_bus_op",
        null=True,
    )
    is_pos_connected = models.BooleanField(default=True)
    printing_enabled = models.BooleanField(default=False)
    trips_access = models.BooleanField(default=True)
    access_password = models.CharField(max_length=255, null=True, blank=True)
    ticket_header = models.CharField(max_length=255, null=True, blank=True)
    ticket_footer = models.CharField(
        max_length=255,
        default="ApniBus वॉलेट में ₹250 तक जीतें, नीचे दिए नंबर पर कॉल करें",
        null=True,
        blank=True,
    )
    is_ticket_amount_editable = models.BooleanField(default=False)
    apply_concession = models.BooleanField(default=True)
    subscription_pending = models.BooleanField(default=False)
    show_seat_type = models.BooleanField(default=False)
    pos_lock = models.BooleanField(default=False)
    show_previous_town = models.BooleanField(default=False)
    print_bus_number = models.BooleanField(default=False)
    show_passenger_header = models.BooleanField(default=False)
    bus_layout_json = models.JSONField(null=True, blank=True)
    is_layout = models.BooleanField(default=False, null=True, blank=True)
    layout_type = models.CharField(max_length=255, null=True, blank=True)
    long_press = models.BooleanField(default=False, null=True, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGES, default=HINDI)
    normal_seats_capacity = models.PositiveIntegerField(default=0)
    single_sleeper_capacity = models.PositiveIntegerField(default=0)
    sharing_sleeper_capacity = models.PositiveIntegerField(default=0)
    upper_single_sleeper_capacity = models.PositiveIntegerField(default=0)
    upper_sharing_sleeper_capacity = models.PositiveIntegerField(default=0)
    route_last_updated = models.PositiveIntegerField(default=0, null=True, blank=True)
    online_app_booking_commission = models.CharField(
        max_length=255,
        choices=ONLINE_APP_BOOKING_COMMISSION,
        null=True,
        default=PERCENTAGE,
    )
    end_trip_report_type = models.CharField(
        max_length=255,
        choices=END_TRIP_REPORT_TYPE,
        null=True,
        default=END_TRIP,
    )
    qr_booking_commission = models.CharField(
        max_length=255, choices=QR_BOOKING_COMMISSION, null=True, default=FULL_AMOUNT
    )
    bd_name = models.CharField(null=True, blank=True)
    bd_number = models.CharField(null=True, blank=True)
    is_standing_ticketing_enabled = models.BooleanField(
        null=True, blank=True, default=False
    )
    can_cut_standing_ticket_before_seat_fill = models.BooleanField(
        null=True, blank=True, default=False
    )
    is_service_flow_enabled = models.BooleanField(null=True, blank=True, default=False)
    can_cut_standing_ticket_only_on_start_town = models.BooleanField(
        null=True, blank=True, default=False
    )
    is_commuter_ticket_pop_up_enabled = models.BooleanField(
        null=True, blank=True, default=True
    )
    dangling_seat_text = models.CharField(null=True, blank=True)
    individual_concession_enabled = models.BooleanField(
        default=False, null=True, blank=True
    )
    is_card_payment_enabled = models.BooleanField(default=False, null=True, blank=True)
    payment_qr_code = models.CharField(
        max_length=500, default="", null=True, blank=True
    )
    language_code = models.CharField(max_length=4, default="hi", null=True, blank=True)
    is_seat_queue_system_enabled = models.BooleanField(
        default=True, null=True, blank=True
    )

    show_from_to_header = models.BooleanField(default=True, null=True, blank=True)
    show_date_time = models.BooleanField(default=True, null=True, blank=True)
    show_bus_number = models.BooleanField(default=True, null=True, blank=True)
    show_ticket_number = models.BooleanField(default=True, null=True, blank=True)
    show_seat_numbers = models.BooleanField(default=True, null=True, blank=True)
    show_concession = models.BooleanField(default=True, null=True, blank=True)

    qr_code_footer = models.CharField(
        default="ApniBus", max_length=255, null=True, blank=True
    )
    ticket_helpline_number = models.CharField(
        default="", max_length=255, null=True, blank=True
    )
    lucky_ticket_number_prefix = models.CharField(max_length=255, null=True, blank=True)

    ticket_footer_image_url = models.CharField(
        default="https://gcpmigratedbuckets.blob.core.windows.net/apnibus-s3/apnibus.jpeg",
        max_length=255,
        null=True,
        blank=True,
    )
    to_print_duplicate_luggage_ticket = models.BooleanField(
        default=False, null=True, blank=True
    )
    to_print_trip_detail_summary = models.BooleanField(
        default=True, null=True, blank=True
    )

    old_visible_towns_count = models.IntegerField(default=0, null=True, blank=True)
    is_custom_ticket_footer_enabled = models.BooleanField(default=False,null=True,blank=True)
    custom_ticket_footer_json = models.JSONField(null=True,blank=True)
    commuter_ticket_pnr_url = models.TextField(default="", null=True, blank=True)
    is_firestore_ticketing_enabled = models.BooleanField(default=False, null=True, blank=True)
    is_name_number_request_feature_enabled = models.BooleanField(default=False, null=True, blank=True)
    is_footer_first_in_custom_layout = models.BooleanField(default=False, null=True, blank=True)

    to_show_digital_ticket_before_print = models.BooleanField(default=False, null=True, blank=True)

    show_to_town_list = models.BooleanField(default=True, null=True, blank=True)
    quick_actions_json = models.JSONField(null=True, blank=True)
    show_quick_action = models.BooleanField(default=False, null=True, blank=True)
    show_ticket_price = models.BooleanField(default=True, null=True, blank=True)
    is_digital_pass_flow_enabled = models.BooleanField(default=False, null=True, blank=True)
    to_ask_phone_number_before_ticket_print = models.BooleanField(default=False, null=True, blank=True)
    to_show_custom_date_picker_before_ticket = models.BooleanField(default=False, null=True, blank=True)
    ticket_price_font_size = models.IntegerField(null=True,blank=True, default=14)
    only_ask_for_phone_if_amount_edited = models.BooleanField(default=False,null=True,blank=True)
    is_phone_number_request_mandatory = models.BooleanField(default=False,null=True,blank=True)
    to_show_conductor_settlement_card = models.BooleanField(default=True,blank=True,null=True)
    to_show_global_ticket_number_in_ticket = models.BooleanField(default=False,blank=True,null=True)
    is_regular_price_ticketing_enabled = models.BooleanField(default=False, null=True, blank=True)

    to_request_location_permission = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "bus_bus"

class ProxyBus(Bus):
    class Meta:
        proxy = True


class BusRoute(PosBaseModel):
    name = models.CharField(max_length=165, null=True, blank=True)
    hindi_name = models.CharField(max_length=165, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    duration_mins = models.PositiveIntegerField(null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    bus = models.ForeignKey(
        Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name="bus_routes"
    )
    is_active = models.BooleanField(default=True, null=True, blank=True)
    operator = models.ForeignKey(
        Operator, on_delete=models.SET_NULL, null=True, blank=True
    )
    language = models.CharField(max_length=50, null=True, blank=True)


    is_disabled = models.BooleanField(default=False, null=True, blank=True)

    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="parent_bus_route")

    class Meta:
        managed = False
        db_table = "timtable_busroute"

class ProxyBusRoute(BusRoute):
    class Meta:
        proxy = True



class Trip(PosBaseModel):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.DO_NOTHING, null=True, blank=True)
    pos_local_id = models.BigIntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_tickets = models.PositiveSmallIntegerField(null=True, blank=True)
    is_settled = models.BooleanField(default=False, null=True, blank=True)
    is_visible_to_operator = models.BooleanField(default=True, null=True, blank=True)
    pending_tickets_in_trip = models.PositiveSmallIntegerField(null=True, blank=True)
    total_pending_tickets = models.PositiveSmallIntegerField(null=True, blank=True)
    version = models.CharField(max_length=20, null=True, blank=True)
    dsn_number = models.CharField(max_length=64, null=True, blank=True)
    old_data = models.BooleanField(default = False, null=True, blank=True)
    is_subscription_amount_calculated = models.BooleanField(default = False, null=True, blank=True)
    operator_id = models.UUIDField(null=True, blank=True)
    conductor_id = models.UUIDField(null=True, blank=True)

    start_trip_lat_lng = models.CharField(max_length=255, null=True, blank=True)
    end_trip_lat_lng = models.CharField(max_length=255, null=True, blank=True)
    
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_visible_to_conductor = models.BooleanField(default=True, blank=True, null=True)
    APP_CHOICES = [
        ('ab_partner', 'AB_PARTNER'),
        ('ab_local', 'AB_LOCAL')
    ]
    app_name = models.CharField(choices= APP_CHOICES, default='ab_partner',null=True,blank=True)
    payable_amount = models.PositiveIntegerField(null=True, blank=True)
    is_settlement_done = models.BooleanField(default=False,null=True,blank=True,db_index=True)
    settlement_trip = models.BooleanField(default=False,null=True,blank=True,db_index=True)
    cash_paid_amount = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    waybill_no = models.IntegerField(null=True, blank=True)

    start_GTN = models.IntegerField(default=0,null=True, blank=True)
    end_GTN = models.IntegerField(default=0,null=True, blank=True)

    class Meta:
        managed = False
        db_table = "trip_trip"

class ProxyTrip(Trip):
    class Meta:
        proxy = True

