from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from phillyleg.models import CouncilMember, CouncilDistrict, CouncilDistrictPlan, LegFile, LegAction

"""
This API is definitely a work in progress.  It is a read-only API through
which you can access council members, districts, and legislation.  If you
have any issues or suggestions, please file an issue on the [GitHub] page,
or contact admin@councilmatic.org.

[GitHub]: https://github.com/codeforamerica/councilmatic
"""

class CouncilmaticAPIViewSet (ReadOnlyModelViewSet):
    paginate_by = 20

    def get_serializer_class(self):
        class TempSerializer (HyperlinkedModelSerializer):
            class Meta:
                model = self.model
        return TempSerializer


class GroupModelMixin (ListModelMixin):
    pksep = ','

    def get_queryset(self):
        queryset = super(ParticularListModelMixin, self).get_queryset()
        pks = self.kwargs.get('pks', None)
        
        if pks:
            pks = pks.split(self.pksep)
            queryset = queryset.filter(pk__in=pks)

        return queryset


class CouncilMemberViewSet (CouncilmaticAPIViewSet):
    model = CouncilMember


class DistrictViewSet (CouncilmaticAPIViewSet):
    model = CouncilDistrict


class DistrictPlanViewSet (CouncilmaticAPIViewSet):
    model = CouncilDistrictPlan


class LegislationViewSet (CouncilmaticAPIViewSet):
    model = LegFile
    def get_serializer_class(self):
        class ActionSerializer (ModelSerializer):
            class Meta:
                model = LegAction
                fields = ('id', 'date_taken', 'description', 'motion', 'acting_body', 'notes')

        class LegislationSerializer (HyperlinkedModelSerializer):
            actions = ActionSerializer()

            class Meta:
                model = LegFile

        return LegislationSerializer


class ActionViewSet (CouncilmaticAPIViewSet):
    model = LegAction


router = DefaultRouter()
router.register('councilmember', CouncilMemberViewSet)
router.register('district', DistrictViewSet)
router.register('districtplan', DistrictPlanViewSet)
router.register('legislation', LegislationViewSet)
router.register('action', ActionViewSet)

# class SubscriberView (views.InstanceModelView):
#     resource = resources.SubscriberResource
#     permissions = [permissions.IsRequestingOwnInfoOrReadOnly]
#     allowed_methods = ['GET']

# class SubscriberListView (views.ListOrCreateModelView):
#     resource = resources.SubscriberResource

# class SubscriptionView (views.InstanceModelView):
#     resource = resources.SubscriptionResource

# class SubscriptionListView (views.ListOrCreateModelView):
#     resource = resources.SubscriptionResource


# class ROListModelView (views.ListModelView):
#     allowed_methods = ['GET']

#     def get_query_kwargs(self, *args, **kwargs):
#         pk_list = kwargs.pop('pk_list', None)
#         qargs = super(ROListModelView, self).get_query_kwargs(*args, **kwargs)

#         if pk_list:
#             pk_list = pk_list.split(',')
#             qargs['pk__in'] = pk_list

#         return qargs

#    def get_description(self):
#        if self.__doc__:
#            return

# class ROInstanceModelView (views.InstanceModelView):
#     allowed_methods = ['GET']

# class CouncilMemberListView (ROListModelView):
#     resource = resources.CouncilMemberResource

# class CouncilMemberInstanceView (ROInstanceModelView):
#     resource = resources.CouncilMemberResource
#     permissions = [IsUserOrIsAnonReadOnly]

# class CouncilDistrictListView (ROListModelView):
#     resource = resources.CouncilDistrictResource

# class CouncilDistrictInstanceView (ROInstanceModelView):
#     resource = resources.CouncilDistrictResource

# class CouncilDistrictPlanListView (ROListModelView):
#     """
#     A district plan represents a particular geographic arrangement of council
#     districts.  Each plan has two important fields:

#     - `districts`: The list of references to district resources
#     - `date`: The date that the district plan went into effect
#     """
#     resource = resources.CouncilDistrictPlanResource

# class CouncilDistrictPlanInstanceView (ROInstanceModelView):
#     resource = resources.CouncilDistrictPlanResource

# class LegFileListView (PaginatorMixin, ROListModelView):
#     resource = resources.LegFileResource

# class LegFileInstanceView (ROInstanceModelView):
#     resource = resources.LegFileResource
