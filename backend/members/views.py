from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MemberProfile
from .serializers import MemberProfileSerializer


@api_view(["GET"])
def members_list(request):
    members = MemberProfile.objects.select_related("user").filter(status="approved")
    serializer = MemberProfileSerializer(members, many=True)
    return Response(serializer.data)


