from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CustomUser
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.State
        fields = '__all__'



class CourtAdditionalToolSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtAdditionalTool
        fields = '__all__'

class CourtAdditionalSerializer(serializers.ModelSerializer):
    tools_court = CourtAdditionalToolSerializer(many=True, read_only=True)
    class Meta():
        model = models.CourtAdditional
        fields = '__all__'

class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtType
        fields = '__all__'

class CourtSerializer(serializers.ModelSerializer):
    additional_court = CourtAdditionalSerializer(read_only=True, many=True)
    state_details = StateSerializer(read_only=True, source='state')
    type_details = CourtTypeSerializer(read_only=True, source='type')
    class Meta():
        model = models.Court
        fields = '__all__'



class BookTimeSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.BookTime
        fields = '__all__'
        
class BookSettingsSerializer(serializers.ModelSerializer):
    tools_details = CourtAdditionalToolSerializer(many=True, read_only=True, source='tools')
    class Meta():
        model = models.BookSetting
        fields = '__all__'


class OverTimeSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.OverTime
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    book_time = BookTimeSerializer(many=True, read_only=True)
    book_setting = BookSettingsSerializer(many=True, read_only=True)
    court_details = CourtSerializer(read_only=True, source='court')
    book_over_time = OverTimeSerializer(read_only=True, many=True)
    class Meta():
        model = models.Book
        fields = '__all__'