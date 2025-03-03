from intergeld.apps.core.serializers import DynamicFieldsModelSerializer
from intergeld.apps.interaccount.serializers.accounts import IntergeldAccountSerializer

from ..models import InterUser


class InterUserSerializer(DynamicFieldsModelSerializer):
    intergeldaccount = IntergeldAccountSerializer(
        read_only=True, fields=["id", "account_number", "account_country"]
    )

    class Meta:
        model = InterUser
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "country",
            "intergeldaccount",
        ]
