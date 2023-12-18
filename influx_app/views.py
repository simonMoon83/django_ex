# influx_app/views.py
from django.http import HttpResponse
from django.shortcuts import render
from influx_app.models import InfluxData
from influxdb_client import InfluxDBClient, Point

def write_to_influxdb():
    # InfluxDB 연결 설정
    url = "http://localhost:8086"
    token = "c4pthjjTblGKx8hp8evNWF-A0gjhX7rM_jN5dBUS70PIQ1OmBmDMMYRHBmTu_UlrQEOL42haopnLBJ4jsZ7Xwg=="
    org = "DW"
    bucket = "local"

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api()

    # 예제 데이터
    data = Point("example_measurement").tag("tag_name", "example_tag").field("value", 20.0)

    # InfluxDB에 데이터 쓰기
    write_api.write(bucket=bucket, org=org, record=data)

    # Django 모델에도 데이터 저장
    InfluxData.objects.create(
        measurement=data._name,
        tag_name=data._tags['tag_name'],
        tag_value='',  # 태그값을 사용하려면 InfluxData 모델에 tag_value 필드를 추가해야 합니다.
        value=data._fields['value']  # Fix here: use _fields instead of fields
    )

def query_influxdb():
    # InfluxDB 연결 설정 (이전 예제에서 작성한 코드와 동일)
    url = "http://localhost:8086"
    token = "c4pthjjTblGKx8hp8evNWF-A0gjhX7rM_jN5dBUS70PIQ1OmBmDMMYRHBmTu_UlrQEOL42haopnLBJ4jsZ7Xwg=="
    org = "DW"
    bucket = "local"

    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    # 예제 쿼리: 모든 measurement의 최근 10개 데이터 조회
    query = f'from(bucket: "{bucket}") |> range(start: -1h) |> limit(n: 10)'
    result = query_api.query(query, org=org)

    # 결과 리스트 생성
    data_list = []
    for table in result:
        for record in table.records:
            data_list.append({
                'time': record['_time'],
                'measurement': record['_measurement'],
                'value': record['_value'],
            })

    # 연결 닫기
    client.close()

    return data_list

def index(request):
    # InfluxDB에 데이터 쓰기
    write_to_influxdb()

    # InfluxDB에서 데이터 조회
    data_list = query_influxdb()

    # 템플릿에 데이터 전달 및 렌더링
    return render(request, 'influx_app/index.html', {'data_list': data_list})