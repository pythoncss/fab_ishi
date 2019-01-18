from flask_appbuilder import AppBuilder, expose, BaseView, has_access, ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from app import db, appbuilder
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from .models import Location, Gender, Employee
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import render_template, Blueprint, request, make_response, jsonify
import requests, tabulate, ast, json

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()

def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()

class EmployeeModelView(ModelView):
    datamodel = SQLAInterface(Employee)
    list_columns = ['name','location.name','personal_phone']
    base_order = ('name', 'asc')
    show_fieldsets = [('Summary', {'fields': ['name', 'gender', 'contact_group','address', 'personal_phone']})]

class GroupLocationView(ModelView):
    datamodel = SQLAInterface(Location)
    related_views = [EmployeeModelView]


class MyView(BaseView):
    route_base = "/api/vi"
    @expose('/empdataa', methods=['GET','POST'])
    def employee_data(self):
        emp_data = session.query(Employee).filter().all()
        li = []
        for x in emp_data:
             mydict = {'Name' : x.name,
		       'Address' : x.address,
                       'Personal_phone': x.personal_phone,
                    }
		   
             li.append(mydict)
        return json.dumps(li)

    
    @expose('/getdata_b', methods=['GET','POST'])
    def get_data_b(self):
        url = "http://localhost:8080/api/vi/empdataa"
        response = requests.request("GET", url)
        data = json.loads(response.text) 
        ult_list = ast.literal_eval(json.dumps(data))
        return self.render_template('output.html', ult_list = ult_list)


    @expose('/getdata_c', methods=['GET','POST'])
    def get_data_c(self):
        url = "http://10.60.37.25:8080/api/v1/empdata" 
        response = requests.request("GET", url)
        data = json.loads(response.text)
        ult_list = ast.literal_eval(json.dumps(data)) 
        return self.render_template('output.html', ult_list = ult_list)


db.create_all()
fill_gender()
appbuilder.add_view(GroupLocationView, "List Location", icon="fa-envelope ", category="Menu")
appbuilder.add_view(EmployeeModelView, "Add Employee", icon="fa-envelope ", category="Menu")

appbuilder.add_view_no_menu(MyView())
appbuilder.add_link("Expose Employee", href='/api/vi/empdataa', icon="fa-folder-open-o", category='Menu')
appbuilder.add_link("List Bangalore Employee", href='/api/vi/getdata_b',icon="fa-envelope ", category='Menu')
appbuilder.add_link("List Chennai Employee", href='/api/vi/getdata_c',icon="fa-envelope ", category='Menu')






