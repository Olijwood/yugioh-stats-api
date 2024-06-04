from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Set, SetSimulatedPriceStats, UserSubmittedSetPrices, SetRankings
# from .utils import SET_CODES_DICT
from .validators import validate_set_code

class SetSerializer(serializers.ModelSerializer):
    price_sterling = serializers.SerializerMethodField(read_only=True)
    price_dollars = serializers.SerializerMethodField(read_only=True)
    the_latest_simulated_stats = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Set
        fields = [
            'pk',
            'title',
            'link',
            'type',
            'price_dollars',
            'price_sterling',
            'the_latest_simulated_stats',
        ]
    def get_price_sterling(self, obj):
        return obj.average_price_in_sterling
    
    def get_price_dollars(self, obj):
        return obj.price_with_dollar_sign
    
    def get_the_latest_simulated_stats(self, obj):
        return obj.get_latest_simulated_stats()
    
class MPSetRankingsSerializer(serializers.ModelSerializer):
    set_code = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SetRankings
        fields = [
            #'set',
            'set_code',
            'ranking_date',

            'mp_ranking',
            'mp_cgv_today',
            'mp_cgv_week',
            'mp_cgv_month',
            'mp_cgv_all_time',
            
            # 'ml_ranking',
            # 'ml_cgv_today',
            # 'ml_cgv_week',
            # 'ml_cgv_month',
            # 'ml_cgv_all_time',
        ]

    def get_set_code(self, obj):
        return obj.set.code
    
class MLSetRankingsSerializer(serializers.ModelSerializer):
    set_code = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SetRankings
        fields = [
            #'set',
            'set_code',
            'ranking_date',
  
            'ml_ranking',
            'ml_cgv_today',
            'ml_cgv_week',
            'ml_cgv_month',
            'ml_cgv_all_time',
        ]

    def get_set_code(self, obj):
        return obj.set.code
    
class UserSubmittedSetPricesSerializer(serializers.ModelSerializer):
    sterling_simulated_price = serializers.SerializerMethodField(read_only=True)
    dollars_simulated_price = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
                view_name='ussp-detail-api',
                lookup_field='pk'
            )
    set_code = serializers.CharField(validators=[validate_set_code])
    class Meta:
        model = UserSubmittedSetPrices
        fields = [
            'url',
            'id',
            'set_code',
            'set_title',
            'simulated_price',
            'dollars_simulated_price',
            'sterling_simulated_price',
        ]
    # def validate_set_code(self, value):
    #     if str(value).upper() not in SET_CODES_DICT:
    #         raise serializers.ValidationError(f'{value} is not a valid set code (eg: \'RA01\')')
    #     return str(value).upper()
    
    def get_update_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('ussp-update-api', kwargs={'pk': obj.pk},
                       request=request)
    
    def get_sterling_simulated_price(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, UserSubmittedSetPrices):
            return None
        return obj.get_simulated_price_in_pounds()
    
    def get_dollars_simulated_price(self, obj):
        return '$%.2f' %(obj.simulated_price)
    

class UserSubmittedSetPricesDetailSerializer(serializers.ModelSerializer):
    sterling_simulated_price = serializers.SerializerMethodField(read_only=True)
    dollars_simulated_price = serializers.SerializerMethodField(read_only=True)
    update_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
                view_name='ussp-detail-api',
                lookup_field='pk'
            )
    class Meta:
        model = UserSubmittedSetPrices
        fields = [
            'url',
            'id',
            'set_code',
            'set_title',
            'update_url',
            'simulated_price',
            'dollars_simulated_price',
            'sterling_simulated_price',
        ]

    def get_update_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('ussp-update-api', kwargs={'pk': obj.pk},
                       request=request)
    
    def get_sterling_simulated_price(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, UserSubmittedSetPrices):
            return None
        return obj.get_simulated_price_in_pounds()
    
    def get_dollars_simulated_price(self, obj):
        return '$%.2f' %(obj.simulated_price)