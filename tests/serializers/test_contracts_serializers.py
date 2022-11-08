import pytest

from danube.contracts.models import Contract, WorkItem
from danube.contracts.serializers import ContractSerializer, WorkItemSerializer


@pytest.mark.django_db
@pytest.mark.skip
def test_contract_serializer(contract_dict):
    serializer = ContractSerializer(data=contract_dict)
    assert serializer.is_valid()
    serializer.save()
    assert type(serializer.instance) is Contract


@pytest.mark.django_db
def test_work_item_serializer(work_item_dict):
    serializer = WorkItemSerializer(data=work_item_dict)
    serializer.is_valid()
    serializer.save()
    assert type(serializer.instance) is WorkItem
