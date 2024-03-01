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

class CourtTypeTSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtTypeT
        fields = '__all__'

class CourtImageSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtImage
        fields = '__all__'

class CourtVideoSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtVideo
        fields = '__all__'


class CourtFeatureSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CourtFeature
        fields = '__all__'

class CourtSerializer(serializers.ModelSerializer):
    user_court = UserSerializer(read_only=True, source='user')
    additional_court = CourtAdditionalSerializer(read_only=True, many=True)
    state_details = StateSerializer(read_only=True, source='state')
    court_types = CourtTypeSerializer(read_only=True, source='type')
    court_types2 = CourtTypeTSerializer(read_only=True, source='type2')
    court_image = CourtImageSerializer(read_only=True, many=True)
    court_video = CourtVideoSerializer(read_only=True, many=True)
    court_features = CourtFeatureSerializer(read_only=True, many=True)
    class Meta():
        model = models.Court
        fields = '__all__'



class BookSerializer_for_times(serializers.ModelSerializer):
    user_details = UserSerializer(read_only=True, source='user')
    class Meta():
        model = models.Book
        fields = '__all__'

class BookTimeSerializer(serializers.ModelSerializer):
    book_time = BookSerializer_for_times(read_only=True, source='book')
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




class SettingSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Setting
        fields = '__all__'