from django.shortcuts import render
import pandas as pd
from rest_framework.authentication import get_authorization_header
# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from .models import dayOfWorks, conctereDays, EmployeeOwners, Tokens, Accounts, Auths, Clients
from .serializers import TodoSerializer

dttm={'week':7, 'month':30}

class ListTodo(generics.ListAPIView):
    queryset = dayOfWorks.objects.all()
    serializer_class = TodoSerializer

@api_view(['GET'])
def api_root(request, format=None):
  try:
    auth=get_authorization_header(request).decode('utf8')
    auth=Auths.objects.filter(tokens__access=auth.split(' ')[1]).first()
    if (auth==None):
       return Response (status=404, data={'response': None, 'status':{'code':404, 'message':'User not found'}})
   # auth=Tokens.objects.filter(access=auth.split(' ')[1]).first()
    account=Accounts.objects.filter(id_user=auth.id).first()
    staff=EmployeeOwners.objects.filter(id_owner=account.id).values('id').first().values()

    engine=create_engine('postgresql://postgres:2537300@185.220.35.179:5432/postgres', echo=False)
    data=pd.read_sql_table('dayOfWorks',con=engine, schema='public')
    d=datetime.now()-timedelta(days=dttm[request.query_params['dttm']])
    d1=datetime.now()

    data=data.loc[(data['accountId'].isin(staff))]
    concrete=pd.read_sql_table('conctereDays',con=engine, schema='public')
    client=pd.read_sql_table('Clients',con=engine, schema='public')
    data=data.merge(concrete, how='inner', left_on=['id'], right_on=['daysof'])
    data=data.merge(client, how='left', left_on=['client_id'], right_on=['id'])
    answer={}
    cancel=data.loc[data['iscanceled']==True]
    price=data['price'].sum()
    avg=data.loc[data['iscanceled']==False]
    mean=avg['price'].mean()
    all=data.loc[(data['dttm_start']<datetime.now()-timedelta(days=10))]
    all=set(all['client_id'].to_list())
    new=set(data.loc[(data['dttm_start']>datetime.now()-timedelta(days=10))]['client_id'].to_list())
    count_new=0
    for a in new:
        if a not in all:
            count_new+=1
    answer={'count':len(data.index), 'cancelled':len(cancel), 'price':price, 'new':count_new, 'avg':mean, 'confirm': len(avg.index)}
   # data=data.loc[data['dttmStart']<datetime.now()]
    return Response(data={'responce':answer, 'status':{'code':200, 'message':None}},status=200)
  except Exception as e:
      print(str(e))

class DetailTodo(generics.RetrieveAPIView):
    queryset = dayOfWorks
  #  queryset=dayOfWorks.objects.all()
    serializer_class = TodoSerializer
