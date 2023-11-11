from rest_framework import serializers

from .models import Report


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('publisher', "title", "region", "city", "start_date", "end_date", "published", 'measurements_set')
        depth = 2

    publisher = serializers.CharField()
