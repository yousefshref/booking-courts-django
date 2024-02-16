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

class CourtSerializer(serializers.ModelSerializer):
    state_details = StateSerializer(read_only=True, source='state')
    class Meta():
        model = models.Court
        fields = '__all__'

class CourtAdditionalSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtAdditional
        fields = '__all__'

class CourtAdditionalToolSerializer(serializers.ModelSerializer):
    court_additional_details = CourtAdditionalSerializer(read_only=True, source='court_additional')
    class Meta():
        model = models.CourtAdditionalTool
        fields = '__all__'




class BookSerializer(serializers.ModelSerializer):
    court_details = CourtSerializer(read_only=True, source='court')
    class Meta():
        model = models.Book
        fields = '__all__'

class BookSettingSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(read_only=True, source='book')
    class Meta():
        model = models.BookSetting
        fields = '__all__'
