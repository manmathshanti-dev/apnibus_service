from django.core.management.base import BaseCommand
from django.db.models import Avg, FloatField
from django.db.models.functions import ExtractHour, ExtractMinute, ExtractSecond
from datetime import datetime, timedelta, time

from pos_proxy.models import Trip
from service_app.models.service_model import Service


class Command(BaseCommand):
    help = "Compute average start/end time per bus_route and bus (recent trips only) and update Service table."

    def handle(self, *args, **options):
        today = datetime.today().date()
        seven_days_ago = today - timedelta(days=7)

        trips = Trip.objects.filter(is_deleted=False, start_time__isnull=False, end_time__isnull=False)

        count = 0
        trips_by_group = {}
        for t in trips:
            key = (t.bus_id, t.bus_route_id)
            trips_by_group.setdefault(key, []).append(t)

        def seconds_to_time(seconds):
            if seconds is None:
                return None
            seconds = int(seconds) % 86400
            h = seconds // 3600
            m = (seconds % 3600) // 60
            s = seconds % 60
            return time(h, m, s)

        for (bus_id, bus_route_id), trip_list in trips_by_group.items():
            recent_trips = [t for t in trip_list if t.created_at.date() >= seven_days_ago]
            if not recent_trips:
                continue

            avg_start_seconds = sum(
                t.start_time.hour * 3600 + t.start_time.minute * 60 + t.start_time.second for t in recent_trips
            ) / len(recent_trips)

            avg_end_seconds = sum(
                t.end_time.hour * 3600 + t.end_time.minute * 60 + t.end_time.second for t in recent_trips
            ) / len(recent_trips)

            Service.objects.update_or_create(
                bus_id=bus_id,
                busroute_id=bus_route_id,
                defaults={
                    "start_time": seconds_to_time(avg_start_seconds),
                    "end_time": seconds_to_time(avg_end_seconds),
                    "is_active": True,
                    "is_verified": False,
                },
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Updated {count} Service records using recent trip averages."))
