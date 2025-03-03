from checkstart.apps.core.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from checkstart.apps.student.models import Student,Invoice,AcademicFee

class StudentSerializer(DynamicFieldsModelSerializer):
    departement = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'lastname',
            'matricule',
            'departement',
            'promotion',
            'level',
            'speciality'
        ]
        
    def get_departement(self,obj):
        return obj.get_departement_display()
    
class InvoiceSerializer(DynamicFieldsModelSerializer):
    fee_type = serializers.SerializerMethodField()
    date_of_payement = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'amount',
            'level',
            'fee_type',
            'due_amount',
            'date_of_payement'
        ]
        
    def get_fee_type(self,obj):
        return obj.type.get_category_display()
    
    def get_date_of_payement(self,obj):
        return obj.created_at.date()
    

class FeeSerializer(DynamicFieldsModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = AcademicFee
        fielsa = [
            'id',
            'category',
            'amount',
            'for_level',      
        ]
    
    def get_category(self,obj):
        return obj.get_category_display()