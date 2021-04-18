from django.shortcuts import render
import pandas as pd
import numpy as np
from rest_framework.authentication import get_authorization_header
# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from .models import dayOfWorks, conctereDays, EmployeeOwners, Tokens, Accounts, Auths, Clients, StaffService
from .serializers import TodoSerializer

dttm={'week':7, 'month':30}

class ListTodo(generics.ListAPIView):
    queryset = dayOfWorks.objects.all()
    serializer_class = TodoSerializer

def record(data):
    if data['iscanceled']==False and data['price_x']==0:
        data['price_x']=data['price_y']
    elif data['iscanceled']==True:
        data['price_x']=0
    return data

def record_time(data):
    if data['iscanceled']==False:
            if data['dttm_end']<datetime.now():
                data['price_x']=data['price_y']
            else:
                data['price_x']=0
    else:

        data['price_y']=0
    return data

def record_week(data):
    if data['iscanceled']==False:
            if data['dttm_end']>datetime.now()-timedelta(days=14) and data['dttm_end']<datetime.now()-timedelta(days=7):
                data['price_pr']=data['price_y']
                data['price_new']=0
            else:
                data['price_new']=data['price_y']
    else:

        data['price_y']=0
    return data

@api_view(['GET'])
def api_root(request, format=None):
  try:
    auth=get_authorization_header(request).decode('utf8')
    auth=Auths.objects.filter(tokens__access=auth.split(' ')[1]).first()
    if (auth==None):
       return Response (status=404, data={'response': None, 'status':{'code':404, 'message':'User not found'}})
   # auth=Tokens.objects.filter(access=auth.split(' ')[1]).first()
    account=Accounts.objects.filter(id_user=auth.id).first()
    staff=EmployeeOwners.objects.filter(id_owner=account.id).values('id').all()
    staff = [i['id'] for i in staff]
    engine=create_engine('postgresql://postgres:2537300@185.220.35.179:5432/postgres', echo=False)
    data=pd.read_sql_table('dayOfWorks',con=engine, schema='public')
    d=datetime.now()-timedelta(days=dttm[request.query_params['dttm']])
    d1=datetime.now()

    data=data.loc[(data['accountId'].isin(staff))]
    concrete=pd.read_sql_table('conctereDays',con=engine, schema='public')
    service=pd.read_sql_table('Services',con=engine, schema='public')
    concrete=concrete.merge(service, how='left', left_on=['services_id'], right_on=['id'])
    client=pd.read_sql_table('Clients',con=engine, schema='public')
    data=data.merge(concrete, how='inner', left_on=['id'], right_on=['daysof'])
    data=data.merge(client, how='left', left_on=['client_id'], right_on=['id'])
    answer={}
    data_main=data.apply(record, axis=1)
    all_price=data_main.groupby(by=['accountId']).agg({'price_x':np.sum}).to_dict()

    #mean=data.groupby(by=['accountId']).agg({price})
    cancel=data.loc[data['iscanceled']==True]
    complete=data.loc[data['iscanceled']==False]
    cancel=cancel.groupby(by=['accountId'])['iscanceled'].count().to_dict()
    complete=complete.groupby(by=['accountId'])['iscanceled'].count().to_dict()
    ############################
    concrete_c=data.loc[concrete['dttm_start']==datetime.now().date()]
  #  service_c=pd.read_sql_table('Services',con=engine, schema='public')
 #   concrete_c=concrete_c.merge(service, how='left', left_on=['services_id'], right_on=['id'])
  #  data_c=data.merge(concrete_c, how='inner', left_on=['id'], right_on=['daysof'])
    data_c=concrete_c.apply(record, axis=1)
    all_price_c=data_c.groupby(by=['accountId']).agg({'price_y':np.sum}).to_dict()
    current_c=data_c.groupby(by=['accountId']).agg({'price_x':np.sum}).to_dict()
  ######################################
   # price=data['price'].sum()
   # avg=data.loc[data['iscanceled']==False]
  #  mean=avg['price'].mean()
    answer=[]
    for n in staff:
        new_client={}
        all=data.loc[(data['dttm_start']<datetime.now()-timedelta(days=10))& data['accountId']==n]
        all=set(all['client_id'].to_list())
        new=set(data.loc[(data['dttm_start']>datetime.now()-timedelta(days=10))& data['accountId']==n]['client_id'].to_list())
        count_new=0
        for a in new:
            if a not in all:
                count_new+=1


        new_client['sum']=all_price['price_x'][n]
        try:
            new_client['canceled']=cancel[n]
        except:
            new_client['canceled']=0
        new_client['id']=n
        new_client['complete']=complete[n]
        new_client['new']=count_new
        try:
            new_client['current'] = current_c['price_x'][n]/all_price_c['price_x'][n]
        except:
            new_client['current'] = 0
        answer.append(new_client)

  #  answer={'count':len(data.index), 'cancelled':len(cancel), 'price':price, 'new':count_new, 'avg':mean, 'confirm': len(avg.index)}
   # data=data.loc[data['dttmStart']<datetime.now()]
    return Response(data={'responce':answer, 'status':{'code':200, 'message':None}},status=200)
  except Exception as e:
      print(str(e))

@api_view(['GET'])
def api_main(request, format=None):
  try:
    auth=get_authorization_header(request).decode('utf8')
    auth=Auths.objects.filter(tokens__access=auth.split(' ')[1]).first()
    if (auth==None):
       return Response (status=404, data={'response': None, 'status':{'code':404, 'message':'User not found'}})
   # auth=Tokens.objects.filter(access=auth.split(' ')[1]).first()
    account=Accounts.objects.filter(id_user=auth.id).first()
    staff=EmployeeOwners.objects.filter(id_owner=account.id).values('id').all()
    staff = [i['id'] for i in staff]
    engine=create_engine('postgresql://postgres:2537300@185.220.35.179:5432/postgres', echo=False)
    data=pd.read_sql_table('dayOfWorks',con=engine, schema='public')


    data=data.loc[(data['accountId'].isin(staff))]
    concrete=pd.read_sql_table('conctereDays',con=engine, schema='public')
    concrete = concrete.loc[concrete['dttm_start']<datetime.now()]
    service=pd.read_sql_table('Services',con=engine, schema='public')
    concrete=concrete.merge(service, how='left', left_on=['services_id'], right_on=['id'])
    client=pd.read_sql_table('Clients',con=engine, schema='public')
    data=data.merge(concrete, how='inner', left_on=['id'], right_on=['daysof'])
    data=data.merge(client, how='inner', left_on=['client_id'], right_on=['id'])
    answer={}
    data_main=data.apply(record, axis=1)
    all_price=data_main.agg({'price_x':np.sum}).to_dict()
    count=data_main.shape[0]
    #mean=data.groupby(by=['accountId']).agg({price})
    all=data.loc[data['dttm_start']<datetime.now()-timedelta(days=30)]
    all=set(all['client_id'].to_list())
    new=set(data.loc[(data['dttm_start']>datetime.now()-timedelta(days=30))]['client_id'].to_list())
    count_new=0
    for a in new:
            if a not in all:
                count_new+=1
  ######################################
   # price=data['price'].sum()
   # avg=data.loc[data['iscanceled']==False]
  #  mean=avg['price'].mean()
    answer={}
    answer['sum']=all_price['price_x']
    answer['new']=count_new
    answer['orders']=count

  #  answer={'count':len(data.index), 'cancelled':len(cancel), 'price':price, 'new':count_new, 'avg':mean, 'confirm': len(avg.index)}
   # data=data.loc[data['dttmStart']<datetime.now()]
    return Response(data={'responce':answer, 'status':{'code':200, 'message':None}},status=200)
  except Exception as e:
      print(str(e))

@api_view(['GET'])
def get_staff(request, format=None):
  try:
    auth=get_authorization_header(request).decode('utf8')
    auth=Auths.objects.filter(tokens__access=auth.split(' ')[1]).first()
    if (auth==None):
       return Response (status=404, data={'response': None, 'status':{'code':404, 'message':'User not found'}})
   # auth=Tokens.objects.filter(access=auth.split(' ')[1]).first()
    account=EmployeeOwners.objects.filter(id_user=auth.id).first()
   # staff=EmployeeOwners.objects.filter(id_owner=account.id).values('id').first().values()

    engine=create_engine('postgresql://postgres:2537300@185.220.35.179:5432/postgres', echo=False)
    data=pd.read_sql_table('dayOfWorks',con=engine, schema='public')


  #  data=data.loc[(data['accountId'].isin(staff))]
    concrete=pd.read_sql_table('conctereDays',con=engine, schema='public')
    # concrete=concrete.loc[concrete['account_id']==account.id]
    # concrete['date']=concrete['dttm_start'].dt.date
   # t=datetime.strptime(concrete[1]['dttm_end'], '%YY-%mm-%dd %HH:%MM')
    d=datetime.now().date()
    concrete_day=concrete.loc[concrete['dttm_start'].dt.date==datetime.now().date()]
    service=pd.read_sql_table('Services',con=engine, schema='public')
    concrete_day=concrete_day.merge(service, how='left', left_on=['services_id'], right_on=['id'])
    data_d=data.merge(concrete_day, how='inner', left_on=['id'], right_on=['daysof'])
    answer={}
    data_d=data_d.apply(record_time, axis=1)
    all_price_d=data_d.groupby(by=['accountId']).agg({'price_y':np.sum}).to_dict()
    current_d=data_d.groupby(by=['accountId']).agg({'price_x':np.sum}).to_dict()
    #mean=data.groupby(by=['accountId']).agg({price})
    dttm_s=datetime.now()-timedelta(days=14)
    concrete_week=concrete.loc[(concrete['dttm_start']>dttm_s)&(concrete['dttm_start']<datetime.now())]

    concrete_week=concrete_week.merge(service, how='left', left_on=['services_id'], right_on=['id'])
    data_s=data.merge(concrete_week, how='inner', left_on=['id'], right_on=['daysof'])
    answer={}
    data_s=data_s.apply(record_week, axis=1)
    all_price_s=data_s.groupby(by=['accountId']).agg({'price_pr':np.sum}).to_dict()
    current_s=data_s.groupby(by=['accountId']).agg({'price_new':np.sum}).to_dict()
   # price=data['price'].sum()
   # avg=data.loc[data['iscanceled']==False]
  #  mean=avg['price'].mean()
    answer={}
    try:
        answer['now']=int((current_d['price_x'][account.id]/all_price_d['price_y'][account.id])*100)
    except:
        answer['now']=-1

    try:
        answer['week']=int((current_s['price_new'][account.id]/all_price_s['price_pr'][account.id])*100)

    except:
        answer['week']=-1

  #  answer={'count':len(data.index), 'cancelled':len(cancel), 'price':price, 'new':count_new, 'avg':mean, 'confirm': len(avg.index)}
   # data=data.loc[data['dttmStart']<datetime.now()]
    return Response(data={'responce':answer, 'status':{'code':200, 'message':None}},status=200)
  except Exception as e:
      print(str(e))


class DetailTodo(generics.RetrieveAPIView):
    queryset = dayOfWorks
  #  queryset=dayOfWorks.objects.all()
    serializer_class = TodoSerializer
